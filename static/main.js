
window.onload = () => {
    document.getElementById('up-file').addEventListener('change', handleFileSelect, false);
}


//backend communication
function sendData() {

    // postCsvFile(uploadedFile, (responseText) => { try {
    //         requestCharts(JSON.parse(responseText));
    //     } catch (error) {
    //         clearScreenAndDisplayErrorMessage("Error parsing the data, make sure the .csv file has a correct format.")
    //     }
    // });

    // can either send the file or it's content

    console.log(uploadedData);
    
    postCsvData(uploadedData, (responseText) => {
        try {
            requestCharts(JSON.parse(responseText));
        } catch (error) {
            clearScreenAndDisplayErrorMessage("Error parsing the data, make sure the .csv file has a correct format.")
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
        setTimeout(() => { document.getElementById(parentId).innerHTML = this.responseText; }, delay);
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
function startSpinner(parentId) {
    let spinnerHtml = `<div class="lds-hourglass"></div>`
    document.getElementById(parentId).innerHTML = spinnerHtml;
}

function clearScreenAndDisplayErrorMessage(err) {

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



//test data
function loadTestData() {

    document.querySelector(".file-msg").innerHTML = "dummy_sensor_data.csv";
    window.uploadedData =
`Temp 1,Temp 2,Temp 3,Umiditate 1,Umiditate 2,Umiditate 3,Viteza 1,Prezenta 1,Prezenta 2,Data,,
8.41,1,1,15,80,55,0.01,0,1,12:00:00 AM,,1
9.09,-4.16,9,16,81,54,0.01,0,1,12:00:10 AM,,2
1.41,-9.9,20,17,82,54,0.01,0,1,12:00:20 AM,,3
-7.57,-6.54,31,18,83,55,0.01,0,1,12:00:30 AM,,4
-9.59,2.84,36,19,83,51,0.01,0,1,12:00:40 AM,,5
-2.79,9.6,6,20,83,51,0.01,0,1,12:00:50 AM,,6
6.57,7.54,9,21,83,50,0.01,0,1,12:01:00 AM,,7
9.89,-1.46,6,22,83,53,0.03,0,1,12:01:10 AM,,8
4.12,-9.11,25,23,83,54,0.05,0,1,12:01:20 AM,,9
-5.44,-8.39,17,24,83,53,0.07,0,1,12:01:30 AM,,10
-10,0.04,37,25,83,51,0.09,0,1,12:01:40 AM,,11
-5.37,8.44,9,26,83,55,0.11,0,0,12:01:50 AM,,12
4.2,9.07,15,27,83,55,0.13,0,0,12:02:00 AM,,13
9.91,1.37,27,28,83,50,0.15,0,0,12:02:10 AM,,14
6.5,-7.6,8,29,83,55,0.17,0,0,12:02:20 AM,,15
-2.88,-9.58,38,30,83,53,0.19,0,0,12:02:30 AM,,16
-9.61,-2.75,31,31,83,54,0.21,0,0,12:02:40 AM,,17
-7.51,6.6,33,32,83,53,0.23,0,0,12:02:50 AM,,18
1.5,9.89,26,33,83,52,0.25,0,0,12:03:00 AM,,19
9.13,4.08,32,34,83,54,0.27,0,0,12:03:10 AM,,20
8.37,-5.48,15,35,83,54,0.29,0,0,12:03:20 AM,,21
-0.09,-10,6,36,83,52,0.31,0,0,12:03:30 AM,,22`;


}