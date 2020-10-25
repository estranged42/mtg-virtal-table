module.exports = {
  "pages": {
    "index": {
      "entry": "src/main.js",
      "title": 'MTG: Virtual Table'
    }
  },
  "transpileDependencies": [
    "vuetify"
  ],
  configureWebpack: {
    mode: 'development',
    devtool: 'inline-source-map'
  }
}
