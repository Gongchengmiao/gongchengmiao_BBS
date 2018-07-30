function overShow(obj,e) {
    var showDiv = document.getElementById('showDiv');
    var theEvent = window.event|| e;
    var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
    var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
    var x = e.pageX || e.clientX + scrollX;
    var y = e.pageY || e.clientY + scrollY;
    showDiv.style.left = x+'px';
    showDiv.style.top = y+'px';
    showDiv.style.display = 'block';
    //alert(obj.innerHTML);
    showDiv.innerHTML = obj.innerHTML;
}

function outHide() {
    var showDiv = document.getElementById('showDiv');
    showDiv.style.display = 'none';
    showDiv.innerHTML = '';
}


function imgRefresh1() {
    document.getElementById('imgshow').setAttribute("src","img/boy_glasses.jpg");
}
function imgRefresh2() {
    document.getElementById('imgshow').setAttribute("src","img/boy_sport.jpg");
}
function imgRefresh3() {
    document.getElementById('imgshow').setAttribute("src","img/boy_hat.jpg");
}
function imgRefresh4() {
    document.getElementById('imgshow').setAttribute("src","img/girl_rollhair.jpg");
}
function imgRefresh5() {
    document.getElementById('imgshow').setAttribute("src","img/girl_shorthair.jpg");
}
function imgRefresh6() {
    document.getElementById('imgshow').setAttribute("src","img/girl_silent.jpg");
}

function nowFitShow() {
    document.getElementById('imgnow').setAttribute("src",document.getElementById('imgshow').src);
}

function showFitNow() {
    document.getElementById('imgshow').setAttribute("src",document.getElementById('imgnow').src);
}

$('#boyg').on('click', imgRefresh1);
$('#boys').on('click', imgRefresh2);
$('#boyh').on('click', imgRefresh3);
$('#girlr').on('click', imgRefresh4);
$('#girlsh').on('click', imgRefresh5);
$('#girlsi').on('click', imgRefresh6);
$('#imgsave').on('click', nowFitShow);
$('#changeimg').on('click', showFitNow);



function loadData()
{
    var xmlhttp;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET","x_mailbox_demo.html",false);
    xmlhttp.send();
    document.getElementById("update").innerHTML=xmlhttp.responseText;
}




function talk() {

    var Words = document.getElementById("chatshow");
    var TalkWords = document.getElementById("chatinput");
    var TalkSub = document.getElementById("talksub");
    var date = new Date();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var currentTime =  hour + ":" + minute;
        //定义空字符串
        var str = "";
        if(TalkWords.value == ""){
            return;
        }
        str =   '<div class="right">' +
                '<div class="author-name">' +
                '<a href="x_personal_page_show_demo.html" target="_blank" style="color: #0d8ddb"><strong>我</strong></a>' +
                '<small class="chat-date">' +
                 currentTime +
                '</small>' +
                '</div>' +
                '<div class="chat-message">' +
                 TalkWords.value +
                '</div>' +
                '</div>'
                +'<br>';
        Words.innerHTML = Words.innerHTML + str;
        Words.scrollTop = Words.scrollHeight;
    TalkWords.value = "";
}


function Recieve() {
    var Words = document.getElementById("chatshow");
    var str = "";
    var str2 = str;

    function getJson()
    {
        $.getJSON("js/userinfo.json", function (data) {
            $.each(data, function (infoIndex, info) {
                str =   '<div class="left">' +
                        '<div class="author-name">' +
                        '<a href="x_personal_page_show_demo.html" target="_blank" style="color: #0d8ddb"><strong>info["name"]</strong></a>' +
                        '<small class="chat-date">' +
                        'info["time"]' +
                        '</small>' +
                        '</div>' +
                        '<div class="chat-message active">' +
                        'info["message"]' +
                        '</div>' +
                        '</div>'
                        +'<br>';

            });
        });
    }

    if(str2 === str){
        setTimeout("getJson()",1000);
    }
    else {
        str2 = str;
    }

    if (str != "") {
        Words.innerHTML = Words.innerHTML + str;
        Words.scrollTop = Words.scrollHeight;
    }
    setTimeout("Recieve()",1000);
}
