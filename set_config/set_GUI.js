const socket = new WebSocket("ws://localhost:5003");
let conf = new Array();

function onTabKey(e, obj){
    if(e.keyCode == 9){
        e.preventDefault();
        var pos = obj.selectionStart;
        var left = obj.value.substr(0, pos);
        var right = obj.value.substr(pos, obj.value.length);

        obj.value = left + "\t" + right;
        obj.selectionEnd = pos+1;
    }
}
document.getElementById("config").onkeydown = function(e){onTabKey(e, this);}

function writeModule(){
    const module = document.getElementById("module").value;
    const position = document.getElementById("position").value;
    const config = document.getElementById("config").value;
    let obj = {module: module, position: position, config: config};
    conf.push(obj);

    let result = document.getElementById("output");
    for(let key in conf){
        result.value += "{\n";
        result.value += "\tmodule: "+conf[key].module + "\n";
        result.value += "\tposition: "+conf[key].position + "\n";
        result.value += "\tconfig:{\n"+conf[key].config + "\n\t}\n";
        result.value += "},\n";
    }

}

function sendResult(){
    let result = document.getElementById("output");
    result.value = conf[0].module
}