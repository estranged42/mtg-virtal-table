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
  chainWebpack: config => {
    if (process.env.NODE_ENV === 'production') {
      config
          .plugin('html-index')
          .tap(args => {
              args[0].template = "public/index-prod.html";
              return args;
          })
    }
  }
}
