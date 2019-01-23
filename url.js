const malScraper = require('mal-scraper')

const name = 'Shoujo Kageki'
var string = ''
var white = ' '
var key = 'synonyms'
var keyname = 'title'
process.argv.forEach(function(val, index, array) {
    if(index >=2)
    {
	console.log(val)
	malScraper.getInfoFromURL(val)
    	    .then((data) => console.log(data[keyname] + " " + data[key]))
    	    .catch((err) => console.log(err))
}
});
