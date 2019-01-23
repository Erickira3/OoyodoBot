const malScraper = require('mal-scraper')

const name = 'Shoujo Kageki'
var string = ''
var white = ' '
var keyname = 'title'
var keyurl = 'link'
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
var typs = string.split(',')
await malScraper.getSeason(typs[0].trim(), typs[1].trim())
    .then((data) => data2 = data)
    .catch((err) => console.log(err));
    
for(var i in data2["TV"])
    {
        console.log("" + data2["TV"][i][keyname] + " $ " + data2["TV"][i][keyurl] + " | ")
    }
}

demo();
