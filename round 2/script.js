setTimeout(function() {
    document.getElementById("animate").style.display = "none";
    document.getElementsByClassName("sidebar")[0].style.display = "block";
    document.getElementsByClassName("container-box")[0].style.display = "block";
    load_notes();
    // document.getElementById("expanded").style.right = "-9000px";
    // document.getElementById("expanded").style.right = "-1000px";
}, 0000);

function save_note() {
    let title = document.getElementById("title").value;
    let note = document.getElementById("autoresizing").value;
    a = new Date();
    date =
        a.getDay() +
        "." +
        a.getMonth() +
        "." +
        a.getYear() +
        " - " +
        a.getHours() +
        ":" +
        a.getMinutes();
    console.log(title, note);

    if (localStorage.getItem("diarybook") == null) {
        itemjsonarray = [];
        itemjsonarray.push([title, date, note, uploaded_image]);
        localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));
    } else {
        itemjsonarraystr = localStorage.getItem("diarybook");
        itemjsonarray = JSON.parse(itemjsonarraystr);
        itemjsonarray.push([title, date, note, uploaded_image]);
        localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));
    }
    uploaded_image = "";
    console.log("item added");
    load_notes();
}

function load_notes() {
    if (localStorage.getItem("diarybook") == null) {
        itemjsonarray = [];
        localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));
    } else {
        itemjsonarraystr = localStorage.getItem("diarybook");
        itemjsonarray = JSON.parse(itemjsonarraystr);
    }
    let card = "";
    itemjsonarray.forEach((element, index) => {
        card =
            card +
            '<div class="card" onclick="enlarge(this)"><div class="imgBx"><img src="static/enlarged.png" alt=""></div><div class="content"><div><h3 class="card-title">' +
            element[0] +
            '</h3><h2 class="card-date">' +
            element[1] +
            '</h2><p class="card-note">' +
            element[2] +
            '</p><img src="' +
            element[3] +
            '" alt="" class="card-img"><p class="card-id" style="color:transparent;">' +
            index +
            "</p></div></div></div>";
        // console.log(element[0], element[1], element[2]);
    });
    document.getElementById("card-container").innerHTML = card;

    console.log("notes loaded....");
}

function remove_expand() {
    var i = document.getElementById("expand-delid").innerHTML;
    i = parseInt(i);
    console.log(typeof index);
    if (i == 0) {
        clear_all();
    }
    itemjsonarraystr = localStorage.getItem("diarybook");
    itemjsonarray = JSON.parse(itemjsonarraystr);
    itemjsonarray.splice(i, 1);

    localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));

    close_expand();
    load_notes();
}

function clear_all() {
    itemjsonarraystr = localStorage.getItem("diarybook");
    itemjsonarray = JSON.parse(itemjsonarraystr);
    itemjsonarray = [];
    localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));
    load_notes();
}

function validateAndUpload(input) {
    var file = input.files[0];

    if (file) {
        var image = new Image();

        image.onload = function() {
            if (this.width) {
                console.log("Image has width, I think it is real image");
                //TODO: upload to backend
            }
        };

        image.src = URL.createObjectURL(file);
    }
}