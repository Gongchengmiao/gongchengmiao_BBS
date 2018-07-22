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

    var Words = document.getElementById("words");
    var TalkWords = document.getElementById("talkwords");
    var TalkSub = document.getElementById("talksub");

    TalkSub.onclick = function(){
        //定义空字符串
        var str = "";
        if(TalkWords.value == ""){
            // 消息为空时弹窗
            alert("消息不能为空");
            return;
        }
        str = '<div class="metalk">' +
              '<span>' +
              '<a href="x_personal_page_show_demo.html" target="_blank" style="color: #0d8ddb">A</a>' + ":" + TalkWords.value +
              '</span>' +
              '</div>';
        Words.innerHTML = Words.innerHTML + str;
        Words.scrollTop = Words.scrollHeight;
    };
}


function Recieve() {
    var Words = document.getElementById("words");
    var str = "";
    var str2 = str;

    function getJson()
    {
        $.getJSON("js/userinfo.json", function (data) {
            $.each(data, function (infoIndex, info) {
                str = '<div class="othertalk">' +
                    '<span>' +
                    '<a href="x_personal_page_show_demo.html" target="_blank" style="color: #0d8ddb">info["name"]</a>' + ":" + info["message"] +
                    '</span>' +
                    '</div>';

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