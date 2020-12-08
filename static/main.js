
window.onload = () => {
    document.getElementById('up-file').addEventListener('change', handleFileSelect, false);
}


//backend communication
function sendData() {

    // can either send the file or it's content
    // postCsvData(uploadedData, (responseText) => {
    //     requestCharts( JSON.parse(responseText) );
    // });

    postCsvFile(uploadedFile, (responseText) => {
        try {
            requestCharts(JSON.parse(responseText));
        } catch (error) {
            clearScreenAndDisplayErrorMessage( "Error parsing the data, make sure the .csv file has a correct format." )
        }

    });
}


function requestCharts(postResponse) {
    requestAndDisplaychart(postResponse.charts.html.temperature, "temperature-chart", 500);
    requestAndDisplaychart(postResponse.charts.html.humidity, "humidity-chart", 1000);
    requestAndDisplaychart(postResponse.charts.html.speed, "speed-chart", 700);

    requestAndDisplaychart(postResponse.charts.html.presence1, "presence1-chart", 1000);
    requestAndDisplaychart(postResponse.charts.html.presence2, "presence2-chart", 2300);
}
 
function requestAndDisplaychart(url, parentId, delay) {
    startSpinner(parentId);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function () {
        setTimeout( ()=>{ document.getElementById(parentId).innerHTML = this.responseText; } , delay );
    };
    xhr.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    xhr.send(null);
}

function postCsvData(data, callback) {

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/csv_data/text');
    xhr.onload = function () {
        callback(this.responseText);
    };
    xhr.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    xhr.send(data);
}

function postCsvFile(file, callback) {

    let formData = new FormData();
    formData.append("file", file, "data.csv");

    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/csv_data/file");
    xhr.onload = function () {
        callback(this.responseText);
    };
    xhr.send(formData);
}


// changing the gui
function startSpinner(parentId){
    let spinnerHtml = `<div class="lds-hourglass"></div>`
    document.getElementById(parentId).innerHTML = spinnerHtml;
}

function clearScreenAndDisplayErrorMessage(err){

    document.getElementById("temperature-chart").innerHTML = "";
    document.getElementById("humidity-chart").innerHTML = "";
    document.getElementById("speed-chart").innerHTML = "";
    document.getElementById("presence1-chart").innerHTML = "";
    document.getElementById("presence2-chart").innerHTML = "";

    alert(err);
}
 

// upload file handler
function handleFileSelect(evt) {

    var file = evt.target.files[0];
    window.uploadedFile = file;

    var reader = new FileReader();

    reader.onload = (function (file) {
        return function (data) {
            console.log("fle uploaded", file);
            window.uploadedData = data.target.result;
        };
    })(file);

    reader.readAsText(file);
}

var $fileInput = $('.file-input');
var $droparea = $('.file-drop-area');

// highlight drag area
$fileInput.on('dragenter focus click', function () {
    $droparea.addClass('is-active');
});

// back to normal state
$fileInput.on('dragleave blur drop', function () {
    $droparea.removeClass('is-active');
});

// change inner text
$fileInput.on('change', function () {
    var filesCount = $(this)[0].files.length;
    var $textContainer = $(this).prev();

    if (filesCount === 1) {
        // if single file is selected, show file name
        var fileName = $(this).val().split('\\').pop();
        $textContainer.text(fileName);
    } else {
        // otherwise show number of files
        $textContainer.text(filesCount + ' files selected');
    }
});
