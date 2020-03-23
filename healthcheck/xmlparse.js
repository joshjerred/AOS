/*var parser, xmlDoc;
*var text = ["telemetrydata.xml"];


//this obviously needs recursion, but I don't know javascript
parser = new DOMParser();
xmlDoc = parser.parseFromString(text,"text/xml");
window.onload = function what(){

document.getElementById("lockhealth").innerHTML =
xmlDoc.getElementsByTagName("lockhealth")[0].childNodes[0].nodeValue;

document.getElementById("lat").innerHTML =
xmlDoc.getElementsByTagName("latitude")[0].childNodes[0].nodeValue;
document.getElementById("lon").innerHTML =
xmlDoc.getElementsByTagName("longitude")[0].childNodes[0].nodeValue;
document.getElementById("gpsalt").innerHTML =
xmlDoc.getElementsByTagName("gpsalt")[0].childNodes[0].nodeValue;
document.getElementById("gpsspeed").innerHTML =
xmlDoc.getElementsByTagName("gpsspeed")[0].childNodes[0].nodeValue;
document.getElementById("gpsclimb").innerHTML =
xmlDoc.getElementsByTagName("gpsclimb")[0].childNodes[0].nodeValue;
};
*/
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        myFunction(this);
    }
};
xhttp.open("GET", "telemetrydata.xml", true);
xhttp.send();

function myFunction(xml) {
    var xmlDoc = xml.responseXML;
    document.getElementById("lat").innerHTML =
    xmlDoc.getElementsByTagName("lattitude")[0].childNodes[0].nodeValue;
}
