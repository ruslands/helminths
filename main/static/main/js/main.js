var a = 0, b = 0;

function eye(){
    if (b == 0){
        document.getElementsByClassName("label_PassEye")[0].style.background = "url('/static/main/img/eye-o.png')";
        document.getElementsByClassName("label_PassEye")[0].style.backgroundSize = "cover";
        b++;
    }
    else if (b == 1){
        document.getElementsByClassName("label_PassEye")[0].style.background = "url('/static/main/img/eye-c.png')";
        document.getElementsByClassName("label_PassEye")[0].style.backgroundSize = "cover";
        b--;
    }
};

function changePic(){
    if (a == 0){
    document.getElementsByClassName("label_left")[0].style.background = "url('/static/main/img/lt.png')";
    document.getElementsByClassName("label_left")[0].style.backgroundSize = "cover";
    document.getElementsByClassName("label_right")[0].style.background = "url('/static/main/img/rf.png')";
    document.getElementsByClassName("label_right")[0].style.backgroundSize = "cover";
    document.getElementsByClassName("gendert")[0].style.color = '#5D51C6';
    document.getElementsByClassName("gendert")[1].style.color = '#000';
    a++;
    }
    else if (a == 1){
        document.getElementsByClassName("label_left")[0].style.background = "url('/static/main/img/lf.png')";
        document.getElementsByClassName("label_left")[0].style.backgroundSize = "cover";
        document.getElementsByClassName("label_right")[0].style.background = "url('/static/main/img/rt.png')";
        document.getElementsByClassName("label_right")[0].style.backgroundSize = "cover";
        document.getElementsByClassName("gendert")[1].style.color = '#5D51C6';
        document.getElementsByClassName("gendert")[0].style.color = '#000';
        a--;
    }
}
