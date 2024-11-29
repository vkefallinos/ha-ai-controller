# Home Assistant AI Controller

A powerful HACS integration that uses Anthropic's Claude AI to control your home automation system. The AI can create scenes, automations, introspect Zigbee entities, and create triggers based on natural language requests.

## Features

- Full home control via Claude AI
- Creation of scenes and automations
- Zigbee device introspection
- Natural language processing of home automation requests
- Real-time UI showing AI actions and responses
- Tool-based architecture for precise control

## Installation

1. Make sure you have [HACS](https://hacs.xyz/) installed in your Home Assistant instance
2. Add this repository to HACS:
   - Go to HACS > Integrations
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add the URL of this repository
   - Select "Integration" as the category

3. Install the integration through HACS
4. Restart Home Assistant
5. Add the integration through the Home Assistant UI:
   - Go to Configuration > Integrations
   - Click the "+" button
   - Search for "AI Controller"
   - Follow the configuration steps

## Configuration

You'll need an API key from Anthropic to use this integration. You can get one by:

1. Going to https://console.anthropic.com/
2. Creating an account or signing in
3. Generating an API key

During the integration setup, you'll be asked to provide:
- Your Anthropic API key
- (Optional) The Claude model to use (defaults to claude-3-sonnet-20240229)

## Usage

Once installed, you can interact with the AI through:

1. The dedicated UI panel in Home Assistant
2. Send natural language requests like:
   - "Create a scene for movie night that dims the lights and turns on the TV"
   - "Set up an automation to turn on the porch light at sunset"
   - "Show me all my Zigbee devices"
   - "Create a trigger that notifies me when the temperature drops below 20°C"

The AI will:
1. Process your request
2. Execute the necessary actions using the available tools
3. Show you the results in real-time
4. Handle any errors gracefully

## Development

To set up the development environment:

1. Clone this repository
2. Install frontend dependencies:
```bash
cd custom_components/ha_ai_controller/frontend
npm install
npm run build
```

3. Copy the `custom_components/ha_ai_controller` directory to your Home Assistant `custom_components` directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
