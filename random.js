const malScraper = require('mal-scraper')

const name = 'Shoujo Kageki'
var string = ''
var white = ' '
var keyname = 'title'
var keyurl = 'url'
var data2 = ''

process.argv.forEach(function(val, index, array) {
    if(index >=2)
        {
	        string = string.concat(val);
		string = string.concat(white);
	}
});

async function demo()
{
await malScraper.getInfoFromURL(string)
    .then((data) => data2 = data)
    .catch((err) => console.log(err));
console.log("" + data2[keyname] + " $ " + string)
}

demo();
