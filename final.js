const malScraper = require('mal-scraper')

const name = 'Shoujo Kageki'
var string = ''
var white = ' '
var keysynonyms = 'synonyms'
var keyname = 'title'
var keyurl = 'url'
var data2 = ''
var data3 = []
var urld = []

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
await malScraper.getResultsFromSearch(typs[0])
    .then((data) => data2 = data)
    .catch((err) => console.log(err));
    

for(var i in data2)
    {
    	if((data2[i]["name"].toLowerCase().includes(typs[0].toLowerCase().trim())) && data2[i]["payload"]["media_type"].toLowerCase().includes(typs[1].toLowerCase().trim()))
	{
	    console.log("" + data2[i]["name"] + " $ " + data2[i][keyurl] + " | ")
	}
	else if((data2[i]["payload"]["media_type"].toLowerCase().includes(typs[1].trim())))
	{
	    urld.push(data2[i][keyurl])
	    await malScraper.getInfoFromURL(data2[i][keyurl])
		.then((dat) =>  data3.push(dat))
		.catch((err) => console.log(err))
	}
    }
    for(var i in data3)
    {
    	if((data3[i][keysynonyms].toLowerCase().includes(typs[0].toLowerCase().trim())) || data3[i]["englishTitle"].toLowerCase().includes(typs[0].toLowerCase().trim()))
	{
	    console.log("" + data3[i][keyname] + " $ " + urld[i] + " | ")
	}
    }
}

demo();
