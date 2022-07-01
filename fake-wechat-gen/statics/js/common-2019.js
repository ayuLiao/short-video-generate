var browser = {
    versions: function() {
        var u = navigator.userAgent,
            app = navigator.appVersion;
        return { //移动终端浏览器版本信息 
            trident: u.indexOf("Trident") > -1, //IE内核
            presto: u.indexOf("Presto") > -1, //opera内核
            webKit: u.indexOf("AppleWebKit") > -1, //苹果、谷歌内核
            gecko: u.indexOf("Gecko") > -1 && u.indexOf("KHTML") == -1, //火狐内核
            mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
            ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
            android: u.indexOf("Android") > -1 || u.indexOf("Linux") > -1, //android终端或者uc浏览器
            iPhone: u.indexOf("iPhone") > -1, //是否为iPhone或者QQHD浏览器
            iPad: u.indexOf("iPad") > -1, //是否iPad
            webApp: u.indexOf("Safari") == -1 //是否web应该程序，没有头部与底部
        };
    }(),
    language: (navigator.browserLanguage || navigator.language).toLowerCase()
}

function getOs() {
    var OsObject = "";
    if (isIE = navigator.userAgent.indexOf("MSIE") != -1) {
        return "MSIE";
    }
    if (isFirefox = navigator.userAgent.indexOf("Firefox") != -1) {
        return "Firefox";
    }
    if (isChrome = navigator.userAgent.indexOf("Chrome") != -1) {
        return "Chrome";
    }
    if (isSafari = navigator.userAgent.indexOf("Safari") != -1) {
        return "Safari";
    }
    if (isOpera = navigator.userAgent.indexOf("Opera") != -1) {
        return "Opera";
    }
}

function toDecimal4(val) {
    //金额转换 分->元 保留2位小数 并每隔3位用逗号分开 1,234.56

    var _jj = val.substring(0, 1);
    if (_jj != "+") {
        _jj = '';
    }

    var str = (val / 100).toFixed(2) + '';

    var intSum = str.substring(0, str.indexOf(".")); //.replace( /\B(?=(?:\d{3})+$)/g, ',' );//取到整数部分
    console.log(intSum);
    var dot = str.substring(str.length, str.indexOf(".")) //取到小数部分搜索
    var ret = _jj + intSum + dot;
    return ret;
}

function toDecimal3(val) {
    //金额转换 分->元 保留2位小数 并每隔3位用逗号分开 1,234.56
    var str = (val / 100).toFixed(2) + '';
    var intSum = str.substring(0, str.indexOf(".")).replace(/\B(?=(?:\d{3})+$)/g, ','); //取到整数部分
    var dot = str.substring(str.length, str.indexOf(".")) //取到小数部分搜索
    var ret = intSum + dot;
    return ret;
}

function toDecimal2(x) {
    var f = parseFloat(x);
    if (isNaN(f)) {
        return false;
    }
    var f = Math.round(x * 100) / 100;
    var s = f.toString();
    var rs = s.indexOf('.');
    if (rs < 0) {
        rs = s.length;
        s += '.';
    }
    while (s.length <= rs + 2) {
        s += '0';
    }
    return s;
}

Number.prototype.formatMoney = function(places, symbol, thousand, decimal) {
    places = !isNaN(places = Math.abs(places)) ? places : 2;
    symbol = symbol !== undefined ? symbol : "$";
    thousand = thousand || ",";
    decimal = decimal || ".";
    var number = this,
        negative = number < 0 ? "-" : "",
        i = parseInt(number = Math.abs(+number || 0).toFixed(places), 10) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return symbol + negative + (j ? i.substr(0, j) + thousand : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thousand) + (places ? decimal + Math.abs(number - i).toFixed(places).slice(2) : "");
};

$(function() {

    //初始化手机时间
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();

    //qq表情
    $(qq_emoji).each(function(i, item) {
        var a = '<a title="' + item + '" href="javascript:;"></a>';
        $('.faceBox').append(a);
    });

    var _auto_jilu_ing = false;
    $(".radio-auto-jilu").click(function() {
        var _is_auto = $(this).val();

        if (_is_auto == 0) { //end
            _auto_jilu_ing = false
            return;
        }

        _auto_jilu_ing = true;

        var _top = $(".i-body").scrollTop();
        var _sd = $(".auto-jilu-px").val();
        _sd = parseInt(_sd);
        var _autoScroll = function() {
            if (!_auto_jilu_ing) return;
            _top += _sd;
            $(".i-body").scrollTop(_top);
            setTimeout(_autoScroll, 20);
        };
        _autoScroll();

    });
    $(".radio-del-jilu").click(function() {
        var _is_del = $(this).val();
        if (_is_del == 1) {
            $(".iphone").removeClass("iphone-nodel");
        } else {
            $(".iphone").addClass("iphone-nodel");
        }
    });
    //点击显示表情事件
    $('body').on('click', '.btn-add-face', function() {
        var position = $(this).offset();
        var data_input = $(this).attr('data-input');
        $('#emojiPanel').css({
            //left:position.left,
            top: position.top + 55
        }).toggle();
        $('#emojiPanel').attr('data-input', data_input);
        return false;
    });

    //表情点击事件
    $('body').on('click', '.emojiArea a', function() {
        var t = $(this).attr('title');
        var data_input = $(this).parents('#emojiPanel').attr('data-input');
        insertAtCursor($('.' + data_input).get(0), '[' + t + ']');
    });

    //初始时间
    for (var i = 0; i < 24; i++) {
        var h = i > 9 ? i : '0' + i;
        var s = h == hours ? ' selected' : '';
        $('.slt-hour,.slt-p-hour').append('<option' + s + '>' + h + '</option>');
    }
    for (var i = 0; i < 60; i++) {
        var h = i > 9 ? i : '0' + i;
        var s = h == minutes ? ' selected' : '';
        $('.slt-minite,.slt-p-minite').append('<option' + s + '>' + h + '</option>');
    }

    $('.slt-common').change(function() {
        var val = $(this).find('option:selected').val();
        var _class = $(this).attr('data-class');
        $(this).find('option').each(function(i, item) {
            $('.' + _class).removeClass($(item).val());
        });
        $('.' + _class).addClass(val);

        if (val == 'i-n-user-group') {
            $(".input-common").val("群聊标题(3)");
            $('.i-n-name span').text("群聊标题(3)");
        }

    });

    $('.rd-common').click(function() {
        var val = $(this).val();
        var _class = $(this).attr('data-class');
        if (val == '1') {
            $('.' + _class).show();
        } else {
            $('.' + _class).hide();
        }
    });

    $('.input-common').change(function() {
        var _class = $(this).attr('data-class');
        var val = $.trim($(this).val());
        $('.' + _class).html(val);
    });

    //手机时间选择
    $('.slt-phone-time').change(function() {
        var shi = $('.slt-p-shi option:selected').val();
        var hour = $('.slt-p-hour option:selected').val();
        var minite = $('.slt-p-minite option:selected').val();
        var str = '';

        if (shi != '-') {
            str += shi;
        }
        str += hour + ':';
        str += minite;

        $('.i-top-time').text(str);
    }).change();

    //点击body事件
    $('body').click(function() {
        $('#emojiPanel').hide();
    });

    $('body').on('click', '.btn-rand-face', function() {
        var face_path = './images/face/';
        var num = get_random_num(1, 60);
        var file_name = face_path + (10000 + num) + '.jpg';
        var img = '<img src="' + file_name + '" />';
        $(this).parents('.add-user').find('.a-u-pic-show img').remove();
        $(this).parents('.add-user').find('.a-u-pic-show input').after(img);

        var _class = $(this).attr('data-class');
        if (_class) {
            var obj = $('.' + _class);
            if (obj.get(0).tagName.toLowerCase() == 'img') {
                obj.attr('src', file_name);
            } else {
                obj.css('background-image', 'url(' + file_name + ')');
            }
        }
    });

    $('body').on('click', '.btn-rand-username', function() {
        //var num = get_random_num(4,8);
        var name = randName(); //randomString(num,true);
        $(this).parents('.add-user').find('.a-u-data-name').val(name);
    });


    $("#iphon_width").on("change", function() {
        var num = $(this).val();
        num = parseInt(num);
        if (!isNaN(num) && num > 0) {
            if (num < 320) num = 320;
            $("#iphon_width").text(num + "px");
            $(".iphone").css({
                "width": num + "px"
            });
        }

    });
    $("#iphon_height").on("change", function() {
        var num = $(this).val();
        num = parseInt(num);
        if (!isNaN(num) && num > 0) {
            if (num < 400) num = 400;
            $("#iphon_height").text(num + "px");
            $(".iphone").css({
                "height": num + "px"
            });
        }

    });
    /*
    	//width
        function setWidth(num){
    		num = parseInt(num);
    		$("#iphon_width").text(num+"px");
    		$(".iphone").css({"width":num+"px"});
        }
        $('.slider_bar_width').sGlide({
          'startAt': 640,
          'width': 320,
          'height': 20,
          'unit': 'px',
          // 'image': 'img/knob_.png',
          // 'pill': false,
          'totalRange': [320,1024],
          // 'locked': true,
      
          'colorShift': ['blue', '#7bb560'],
          // 'vertical': true,
          'buttons': true,
          // 'disabled': true,
          drag: function(o){
            setWidth(o.custom);
          },
          onButton: function(o){
            setWidth(o.custom);
          }
        });



    */

    //height
    function setHeight(num) {
        num = parseInt(num);
        $("#iphon_height").val(num);
        $(".iphone").css({
            "height": num + "px"
        });
    }
    $('.slider_bar_height').sGlide({
        'startAt': 1136,
        'width': 320,
        'height': 20,
        'unit': 'px',
        // 'image': 'img/knob_.png',
        // 'pill': false,
        'totalRange': [500, 5000],
        // 'locked': true,

        'colorShift': ['blue', '#7bb560'],
        // 'vertical': true,
        'buttons': true,
        // 'disabled': true,
        drag: function(o) {
            setHeight(o.custom);
        },
        onButton: function(o) {
            setHeight(o.custom);
        }
    });

    //电池滑块
    function setBar(num) {
        if (num <= 20) {
            $('.i-top-berry i em').css('background', '#f30');
        } else {
            $('.i-top-berry i em').css('background', '#000');
        }
        $('.i-top-berry i em').css('width', num + '%');
        num = num.toString();
        var index = num.toString().lastIndexOf('.');
        num = index == -1 ? num : num.substring(0, index);
        $('.i-top-berry-num').text(num + '%');
    }
    $('.slider_bar').sGlide({
        'startAt': 50,
        'width': 300,
        'height': 20,
        'unit': 'px',
        // 'image': 'img/knob_.png',
        // 'pill': false,
        'totalRange': [1, 100],
        // 'locked': true,

        'colorShift': ['#3a4d31', '#7bb560'],
        // 'vertical': true,
        'buttons': true,
        // 'disabled': true,
        drag: function(o) {
            setBar(o.custom);
        },
        onButton: function(o) {
            setBar(o.custom);
        }
    });

    if (is_check_brower && (getOs() != 'Chrome' && getOs() != 'Safari')) {
        //if(is_check_brower){
        var browser = '<div class="browser"><a target="_blank" href="http://rj.baidu.com/soft/detail/14744.html"><span>o(︶︿︶)o 抱歉！您的浏览器不兼容，为了更好的制作效果，请用</span><i></i><em>谷歌浏览器</em><span>&nbsp;打开</span></a><a class="pop-close" href="#">x</a></div>';
        $('body').append(browser);
        $('body').append('<div class="mask"></div>');
        $('.mask').height($(document).height());
    }

    $('.pop-close').click(function() {
        $('.mask,.browser').hide();
        return false;
    });

    $('body').on('click', '.my-image-continue', function() {
        $('.mask,.my-image').hide();
        return false;
    });
});