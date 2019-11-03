/**
 * Testing
 */
import * as readline from 'readline';
declare var require: any

 /**
  * Represents a building on campus where classes may be held
  * code: the code that appears on schedules, eg. BUCH
  * name: full name of building, eg. "Buchanan"
  * address: address of the building, eg. "1866 Main Mall, Vancouver, BC V6T 1Z1"
  */
 interface Building {
     code: string,
     name: string,
     address: string,
 };

 /**
  * A list of buildings on UBC campus
  */
const BUILDING_LIST:Building[] = [
    {
        code: 'HENN',
        name: 'Hennings',
        address: 'Hennings Building, Hennings Bldg, Vancouver, BC V6T 1Z1'
    },
    {
        code: 'DMP',
        name: 'Hugh Dempster Pavillion',
        address: '6245 Agronomy Rd, Vancouver, BC V6T 1Z4'
    },
];

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const Http = new XMLHttpRequest();
const APIKey = ''; //TODO: replace with empty string
let url;
let matrix = [
    ['',                    BUILDING_LIST[0].code, BUILDING_LIST[1].code]
    [BUILDING_LIST[0].code, 0,                     '']
    [BUILDING_LIST[1].code, '',                    0]
]

function main() {
    let distanceMatrixRow = [];
    let buildingAddress1 = BUILDING_LIST[0].address;
    BUILDING_LIST.forEach(building => {

    });

    url = `https://maps.googleapis.com/maps/api/distancematrix/json?origins=${BUILDING_LIST[0].address}&destinations=${BUILDING_LIST[1].address}&key=${APIKey}`;
    Http.open("GET", url);
    Http.send();

}

main();

Http.onreadystatechange= (e) => {
    console.log(Http.responseText);
   // let obj = JSON.parse(Http.responseText);
  //  console.log("Distance is ", obj.rows.elements[0].distance.text);
  //  console.log('Duration is', obj.rows.elements[0].duration.text);
}
