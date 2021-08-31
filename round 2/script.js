setTimeout(function() {
    document.getElementById("animate").style.display = "none";
    document.getElementsByClassName("sidebar")[0].style.display = "block";
    document.getElementsByClassName("container-box")[0].style.display = "block";
    load_notes();
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
        itemjsonarray.push([title, date, note]);
        localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));
    } else {
        itemjsonarraystr = localStorage.getItem("diarybook");
        itemjsonarray = JSON.parse(itemjsonarraystr);
        itemjsonarray.push([title, date, note]);
        localStorage.setItem("diarybook", JSON.stringify(itemjsonarray));
    }
    console.log("item added");
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
            '</p><p id="card-id">' +
            index +
            "</p></div></div></div>";
        console.log(element[0], element[1], element[2]);
    });
    document.getElementById("card-container").innerHTML = card;

    console.log("notes added");
}

function remove_expand() {
    let index = document.getElementById("expand-id").innerHTML;
    itemjsonarray.splice(index, 1);
    localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));
}