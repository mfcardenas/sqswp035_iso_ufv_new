# Frontend

This directory contains the React frontend for the ISO Standards Games application.

## Project Structure

- `public/` - Static files
- `src/` - Source code
  - `components/` - React components
  - `pages/` - Page components
  - `services/` - API services
  - `i18n/` - Internationalization
  - `assets/` - Images, fonts, etc.
  - `styles/` - CSS/SCSS files
  
## Development

The frontend uses React with the following features:
- TypeScript for type safety
- React Router for navigation
- i18next for internationalization
- TailwindCSS for styling
- Axios for API communication

## Building

The frontend is built as part of the main application. The build output is placed in the `dist` directory, which is then served by the FastAPI backend.

```
npm run build
```

## Running in development mode

```
npm run dev
```