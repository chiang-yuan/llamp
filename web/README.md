# Frontend Documentation (web/)

This section is dedicated to explaining the structure and contents of the frontend part of the project, located in the `web/` directory. Here's a breakdown of the main files and folders:

## Folders

- `src/`: The source code of the frontend application.

  - `lib/`: Contains utility modules such as `chatUtils.ts`, which are reused across different parts of the application.
  - `routes/`: Includes the Svelte components and the logic related to different routes of the application, such as `Message.svelte`.

- `static/`: Houses static files like images, which are not processed by Svelte.

## Files

- `Dockerfile.dev`: A Dockerfile for creating a Docker image of the development version of the application.

- `package.json` and `package-lock.json`: Define the project dependencies and other metadata.

- `postcss.config.cjs` and `tailwind.config.ts`: Configuration files related to styling, TailwindCSS and PostCSS in this case.

- `svelte.config.js`: Configuration file for the Svelte application.

- `tsconfig.json`: Configuration file for TypeScript, defining compiler options and other settings.

- `vite.config.ts`: Configuration file for Vite, which is used for building and development purposes.

## Specific File and Folder Details

- `src/lib/`: In this directory, reusable logic and utility functions are defined. For example, `chatUtils.ts` contains functionalities related to chat operations.

- `src/routes/`: This directory includes the UI components of the application. For instance, `Message.svelte` is a component representing a message in the chat application.

- `Dockerfile.dev`: This is specifically used to dockerize the development environment, ensuring that the application runs consistently across different platforms.
