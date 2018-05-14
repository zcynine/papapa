var webPage = require('webpage');
var page = require('webpage').create();

page.open('https://www.baidu.com', function (s) {
  console.log(s);
  phantom.exit();
});
