import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
} from '@mui/material';
import { createConnection, Connection, HassEvent } from 'home-assistant-js-websocket';

interface AIAction {
  tool: string;
  input: any;
  result: any;
  timestamp: string;
}

interface AIError {
  error: string;
  timestamp: string;
}

interface HAEvent extends HassEvent {
  type: string;
  data: any;
}

interface AIResponse {
  success: boolean;
  error?: string;
  response?: string;
}

function App() {
  const [connection, setConnection] = useState<Connection | null>(null);
  const [userInput, setUserInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [actions, setActions] = useState<AIAction[]>([]);
  const [errors, setErrors] = useState<AIError[]>([]);

  useEffect(() => {
    async function initConnection() {
      try {
        const auth = await (window as any).hassConnection;
        const conn = await createConnection({ auth });
        setConnection(conn);

        // Subscribe to AI action events
        conn.subscribeEvents((event: HAEvent) => {
          if (event.type === 'ha_ai_controller_action') {
            setActions(prev => [{
              ...event.data,
              timestamp: new Date().toISOString()
            }, ...prev]);
          } else if (event.type === 'ha_ai_controller_error') {
            setErrors(prev => [{
              ...event.data,
              timestamp: new Date().toISOString()
            }, ...prev]);
          }
        }, 'ha_ai_controller_action');

        conn.subscribeEvents((event: HAEvent) => {
          if (event.type === 'ha_ai_controller_error') {
            setErrors(prev => [{
              ...event.data,
              timestamp: new Date().toISOString()
            }, ...prev]);
          }
        }, 'ha_ai_controller_error');

      } catch (err) {
        console.error('Failed to initialize connection:', err);
      }
    }

    initConnection();
  }, []);

  const handleSubmit = async () => {
    if (!connection || !userInput.trim()) return;

    setIsProcessing(true);
    try {
      const response = await connection.sendMessagePromise({
        type: 'ai_controller/process_request',
        input: userInput,
      }) as AIResponse;

      if (!response.success) {
        setErrors(prev => [{
          error: response.error || 'Unknown error',
          timestamp: new Date().toISOString()
        }, ...prev]);
      }
    } catch (err) {
      console.error('Failed to process request:', err);
      setErrors(prev => [{
        error: String(err),
        timestamp: new Date().toISOString()
      }, ...prev]);
    } finally {
      setIsProcessing(false);
      setUserInput('');
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Home Assistant AI Controller
        </Typography>

        <Paper sx={{ p: 2, mb: 2 }}>
          <TextField
            fullWidth
            multiline
            rows={3}
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Enter your request for the AI..."
            disabled={isProcessing}
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={isProcessing || !userInput.trim()}
          >
            {isProcessing ? <CircularProgress size={24} /> : 'Send Request'}
          </Button>
        </Paper>

        {errors.length > 0 && (
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Errors
            </Typography>
            <List>
              {errors.map((error, index) => (
                <ListItem key={index}>
                  <Alert severity="error" sx={{ width: '100%' }}>
                    <Typography variant="body2" color="text.secondary">
                      {new Date(error.timestamp).toLocaleString()}
                    </Typography>
                    {error.error}
                  </Alert>
                </ListItem>
              ))}
            </List>
          </Paper>
        )}

        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            AI Actions
          </Typography>
          <List>
            {actions.map((action, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={`Tool: ${action.tool}`}
                  secondary={
                    <>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(action.timestamp).toLocaleString()}
                      </Typography>
                      <Typography component="pre" sx={{ mt: 1 }}>
                        Input: {JSON.stringify(action.input, null, 2)}
                      </Typography>
                      <Typography component="pre" sx={{ mt: 1 }}>
                        Result: {JSON.stringify(action.result, null, 2)}
                      </Typography>
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
    </Container>
  );
}

export default App;
