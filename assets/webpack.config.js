var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: {
    main: ['./app.js', './app.scss'],
  },

  output: {
    path: path.resolve('../static/'),
    filename: '[name].js',
  },

  plugins: [
    new ExtractTextPlugin('[name].css')
  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          use: [{
            loader: "css-loader" // translates CSS into CommonJS
          }, {
            loader: "sass-loader" // compiles Sass to CSS
          }],
          // use style-loader in development
          fallback: "style-loader"
        })
      }
    ],
  }
}
