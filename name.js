const malScraper = require('mal-scraper')

const name = 'Shoujo Kageki'
var string = ''
var white = ' '
process.argv.forEach(function(val, index, array) {
    if(index >=2)
    {
	string = string.concat(val);
	string = string.concat(white);
    }
});

console.log(string)
malScraper.getInfoFromName(string)
    .then((data) => console.log(data))
    .catch((err) => console.log(err))

