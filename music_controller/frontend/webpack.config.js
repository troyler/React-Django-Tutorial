// this file bundles all of our JavaScript files, serves it into one file and outputs it to the browser

const path = require("path");
const webpack = require("webpack");

// where is the entry JS file and where should it be outputted?

module.exports = {
  entry: "./src/index.js",    //entry point is at relative path, (so in this case we start here in the frontend directory)
  output: {
    path: path.resolve(__dirname, "./static/frontend"), //path.resolve gets that relative entry path folder and finds static/frontend, where our output file will exist
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    minimize: true,  //this is just minimizing the code to make it quicker to compile by removing unnecssary spaces and such
  },
  plugins: [
    new webpack.DefinePlugin({  //also does a similar thing to optimize
      "process.env.NODE_env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify('production'),
      },
    }),
  ],
};