let fs = require('fs'); 
let parser = require('./gramatica');


fs.readFile('./entrada.txt', (err, data) => {
    if (err) throw err;
    parser.parse(data.toString());
});