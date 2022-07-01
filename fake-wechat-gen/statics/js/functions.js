function insertAtCursor(myField, myValue) {
    //IE support
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
        sel.select();
    }
    //MOZILLA/NETSCAPE support 
    else if (myField.selectionStart || myField.selectionStart == '0') {
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
        // save scrollTop before insert www.keleyi.com
        var restoreTop = myField.scrollTop;
        myField.value = myField.value.substring(0, startPos) + myValue + myField.value.substring(endPos, myField.value.length);
        if (restoreTop > 0) {
            myField.scrollTop = restoreTop;
        }
        myField.focus();
        myField.selectionStart = startPos + myValue.length;
        myField.selectionEnd = startPos + myValue.length;
    } else {
        myField.value += myValue;
        myField.focus();
    }
}

function index_in_array(value, array) {
    for (var i = 0; i < array.length; i++) {
        var v = array[i];
        if (v == value) {
            return i;
        }
    }
    return -1;
}

function replace_qq_emoji(str) {
    str = str.replace(/\[.*?\]/g, function(word) {
        var w = word.replace('[', '').replace(']', '');
        var index = index_in_array(w, qq_emoji);
        return '<img class="qq_emoji" src="./images/qq_emoji/Expression_' + (index + 1) + '@2x.png" />';
    });
    return str;
}
/*
function set_water(){
  var water = $('#iphone .i-water');
  if(!water.length){
    $('#iphone').append('<div class="i-water"></div>');
  }
}*/

// 对Date的扩展，将 Date 转化为指定格式的String 
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符， 
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) 
// 例子： 
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423 
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18 
Date.prototype.format = function(fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

function get_random_num(Min, Max) {
    var Range = Max - Min;
    var Rand = Math.random();
    return (Min + Math.round(Rand * Range));
}

function randomString(len, words) {　　
    len = len || 32;　　
    var $chars = '0123456789';
    if (words) {
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    }　　
    var maxPos = $chars.length;　　
    var pwd = '';　　
    for (i = 0; i < len; i++) {　　　　
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));　　
    }　　
    return pwd;
}

//随机网名
function randName() {
    var num = get_random_num(0, 128);
    var chars = ["\u5fc3\u76f8\u7483", "\u56cd\u9047\u4f60", "\u602a\u6211\u54af", "\u6cd5\u514b\u9c7f", "\u65e0\u4eba\u50cf\u4f60", "\u89c6\u4ed6\u5982\u547d", "\u5708\u59b9\u513f\ufeee", "\u5357\u65b9\u521d\u6625", "\u7eb5\u6211\u60c5\u6df1", "\u4e0d\u7f81\u653e\u7eb5", "\u68a6\u53ca\u6df1\u6d77", "\u5b64\u72ec\u518d\u8bbf", "\u80f8\u8154\u8d77\u98ce", "\u5de6\u6307\u795e\u529f", "\u673a\u667a\u5982\u6211", "\u602a\u96be\u7626.", "\u626c\u7709\u6de1\u770b", "\u522b\u9017\u5be1\u4eba.", "\u4eba\u4e11\u813e\u6c14\u5927", "\u4e10\u5e2e\u8001\u5927\uff01", "\uc7a0\uff08\u5f52\u9690\uff09", "\u56fd\u9645\u96be\u6c11\u2600", "\u592a\u8fc7\u8000\u773c\u2600", "\u4e5f\u662f\u86ee\u62fc\u7684", "\u5e7c\u513f\u56ed\u6253\u624b", "\u563f\u4e36|n\u54bb", "\u4f60\u5728\u641e\u7b11i", "\u5165\u620f\u592a\u6df1i", "\u4e5f\u662f\u9189\u4e86i", "\u6a31\u82b1\u98de", "\u6696\u4e86\u590f\u5929\u84dd\u4e86\u6d77\u00b0", "Royal\u2570\u5927\u61d2\u732b\u2033", "\u5973\u4eba\u30fd\u65e0\u987b\u695a\u695a\u53ef\u601c", "\u5bc2\u5bde\u5982\u96ea", "\u653e\u5f00\u6211\uff0c\u6211\u8981\u88c5\u903c", "www.wwei.cn", "\u5638\u61d9\u502b\u4ef3", "\u542c\u8bf4\u7231\u60c5\u56de\u6765\u8fc7i", "\u613f\u4f60\u7684\u6240\u6709\u6df1\u60c5\u90fd\u4e0d\u88ab\u8f9c\u8d1f", "\u55b5\u5c0f\u54aa\u2121", "\u968f\u9047\u800c\u5b89", "\u5982\u4eba\u996e\u6c34\u51b7\u6696\u81ea\u77e5", "Forever\u3001\u535f\u79bb", "\u522b\u7559\u6211\u5b64\u8eab\u4e00\u4eba", "\u8d8a\u738b\u591f\u8d31", "\u4eba\u5fc3\u592a\u72d7", "\u6b63\u5728\u8f93\u5165\u30fd\u8bf7\u7a0d\u540e", "\u7dc8\u9362d\u0113\u6389\u6e23", "\u534a\u9189\u534a\u9192\u534a\u75f4\u5446", "\u603b\u6709\u5201\u6c11\u60f3\u5bb3\u6715", "\u64e6\u6389\u773c\u6cea\u6211\u4f9d\u65e7\u662f\u738b", "\u5317\u5df7\u00b0", "\u98ce\u7ee7\u7eed\u5439", "\u7cbe\u795e\u5206\u88c2\u60a3\u8005", "\u7c73\u6735\u6735", "\u840c\u5446\u5446\u00b0", "\u2640\u6dfa\u6dfa\u7b11\ufe36", "\u732b\u5c0f\u55b5", "\u840c\u840c\u5154", "\u6cfc\u5987\u8303er", "\u53f2\u73cd\u9999", "\u9017\u5987\u4e73", "\ue822\u5c12\u96e8\u9ede\u2025", "\u251e\u83aa\u72e0\u4e56\u2508", "\u4fbd\u7d38\u89d2", "\u5c0f\u571f\u9017", "\u52a0\u8f7d\u4e2d...99%", "\u5c1b\u5583\u82fd\u3001", "\u795e\u7d93\u8d28\u00b0", "\u7c21\u55ae\u00b7\u611b\u3072", "\u964c\u989c\u5915\u00b0", "\u6d45\u8272\u68f1\u30fdAquarius\u00b0", "\u840c\u840c\u54d2", "\u5c0f\u82b1\u75f4", "\u8461\u5c0f\u8404*", "\u7231\u6210\u788d.", "\u5c0f\u50b2\u5a07", "\u00a4\u5927\u61d2\u866b\u00a4", "\u633d\u537f\u8863.", "\u3093u\u012b\u51ad\u72fc", "\u964c\u58a8\u5b89", "\u83a3\u6182\u8349\u3050", "\u9017\u5987\u4e73", "\u5410\u6ce1\u6ce1o\u03bf\u041e", "\u5928\u5422\u760b", "\u5c0f\u5e78\u798f", "\u521d\u89c1\u4f60", "\u840c\u561f\u561f", "\u613f\u4f60\u5b89", "\u6b87\u9b42\u7834", "\u7ec8\u96be\u9047", "\u989c\u82e5\u60dc", "\u6a31\u82b1\u5df7\u3074", "\u5c10\u510d\u5471", "\u597d\u96be\u7626", "\u6d45\u62fe\u5fc6\u30da", "\u55b5\u5c0f\u54aa(+\ufe4f+)~", "\u80f8\u6bdb\u98d8", "\u5317\u57ce\u8bc0", "\u542c\u96e8\u7720", "\u58dep\u012b\u6c23\u3065", "\u843d\u82b1\u6b8b", "\u51f9\u51f8\u66fcbiu~biu~biu~", "\u602a\u96be\u7626", "24K\u597d\u83c7\u51c9", "\u55b5\u5c0f\u59d0", "\u52a0\u8f7d\u4e2d\u202699.9%", "\u65e0\u4eba\u56cd", "\u6218\u82cd\u7a79", "\u7b28\u5c0f\u86cb", "\u2570\u2606\u5996\u3001\u5c0f\u5b7d\u256f", "\u65e7\u7b11\u8bdd", "\ufe4f\u51c9\u4eba\u5922", "\u5c10\u7c73\u87f2\u221e", "\u6bdb\u6bdb\u87f2", "|\u258d\u9189\u50be\u57ce\u00b0", "\u96be\u62e5\u53cb", "\u4e0d\u8ba8\u56cdi", "\u4e45\u4e0d\u6108", "\u7a7a\u57ce\u51c9", "\u8584\u8377\u7eff\u00b0", "\u51b7\u5915\u989c", "\ufe36\ufe49\u68a6\u503e\u57ce\u3079", "\u03bf\u6f74\u7aa9\u7aa9\u309e", "\u65e7\u4eba\u6b87", "\u683c\u5f0f\u5316", "\u9017\u6bd4\u75c7", "\u94bb\u77f3\u6cea"];

    return chars[num];
}