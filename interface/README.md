# DeepSee visualizations interface

A Vue.js v2 app, styled with the Vuetify Material Design Framework, running on an Express.js server.

Can be built into a standalone desktop application with Electron.

**NOTE FOR macOS/Linux USERS**

- You may need to prefix your terminal commands with `sudo` to grant the system write access to restricted folders.
  - e.g., `sudo npm install -g electron-builder`

## Getting Started

1. Install Node.js v16.x and npm v7.x by visiting <https://nodejs.org/en/>.
2. Open a command window or terminal rooted in this folder.
3. Check that both libraries were installed correctly by running `node -v` and `npm -v`.

## Project setup

```(bash)
npm install
```

### Compiles and hot-reloads for development

```(bash)
npm run serve
```

### Compiles and minifies for production

```(bash)
npm run build
```

## Electron setup

See `package.json` for electron build configuration parameters.

```(bash)
npm install -g electron-builder
```

### Compiles and serves local version

```(bash)
npm run start-electron
```

### Compiles and builds for production

```(bash)
npm run build-electron
```