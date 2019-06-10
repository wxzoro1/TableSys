
function Termselect(){   
    var nSel = document.getElementById("select1");
    var index = nSel.selectedIndex; // 选中索引
    var text = nSel.options[index].text; // 选中文本
        console.log(text)
    $.ajax({ 
        type: 'GET', 
        url: '/s/sctable/'+ text ,
        data:'',
        dataType: 'json' 
    })
    
    .done(function(data){
        render_list(data);
    });
}

function render_list(list) {
    var tbody =  $("#list-tbody").empty();
    for (i in list) {
        var public = list[i];

        var row = $('<tr>');
        $('<td>').text(parseInt(i) + 1).appendTo(row);
        $('<td>').text(public['courseno']).appendTo(row);
        $('<td>').text(public['cname']).appendTo(row);
        $('<td>').text(public['credit']).appendTo(row);
        $('<td>').text(public['property']).appendTo(row);
        $('<td>').text(public['tno']).appendTo(row);
        $('<td>').text(public['tname']).appendTo(row);
        $('<td>').text(public['cla']).appendTo(row);
        $('<td>').text(public['week']).appendTo(row);
        $('<td>').text(public['weekday']).appendTo(row);         
        $('<td>').text(public['period']).appendTo(row);
        $('<td>').text(public['campus']).appendTo(row);
        $('<td>').text(public['building']).appendTo(row);
        $('<td>').text(public['croom']).appendTo(row);

        var btn_edit = $('<button>')
            .text('修改')
            .on( "click", (function(public) {
                return function( event ) {
                    var sn = public['sn'];
                    console.log('edit: ' + sn);
                    edit_public(sn);
                }
            })(public));

        var btn_del = $('<button>')
            .text('删除')
            .on( "click", (function(item) { 
                return function( event ) {
                    delete_public(item['sn']);
                }
            })(public));

        $('<td>').append(btn_edit).append(btn_del).appendTo(row);


        row.appendTo(tbody);
    }
}

function load_list() {

	$.ajax({
        type: 'GET',
  		url: "/s/sctable/",
        data: '',
        dataType: 'json' 
	})
    .done(function(data) {
        console.log(data)
        render_list(data);
    });
}

function get_details(sn) {
  $.ajax({ 
    type: 'get', 
    url: '/subscriptions/' + id,
    data: "subscription[title]=" + encodeURI(value),
    dataType: 'script' 
 	}); 
 
$.ajax({ 
type: 'PUT', 
url: '/subscriptions/' + id,
data: "subscription[title]=" + encodeURI(value),
dataType: 'script' 
}); 

}

function edit_public(sn) {
    function put_public() {
        var item = {};
        var sn = $('#frm-public input[name="sn"]').val();
        item['sn'] = sn;
        item['courseno'] = $('#frm-public input[name="courseno"]').val();
        item['tno'] = $('#frm-public input[name="tno"]').val();
        item['cla'] = $('#frm-public input[name="cla"]').val();
        item['week'] = $('#frm-public input[name="week"]').val();
        item['weekday'] = $('#frm-public select[name="weekday"]').val();
        item['period'] = $('#frm-public select[name="period"]').val();
        item['campus'] = $('#frm-public select[name="campus"]').val();
        item['building'] = $('#frm-public select[name="building"]').val();
        item['croom'] = $('#frm-public input[name="croom"]').val();

        var jsondata = JSON.stringify(item);
        $.ajax({ 
            type: 'PUT', 
            url: '/s/sctable/' + sn,
            data: jsondata,
            dataType: 'json' 
        })
        .done(function(){
            load_list();
            $('#dlg-public-form').hide()
        });

        return false; // 在AJAX下，不需要浏览器完成后续的工作。
    }

    $.ajax({ 
        type: 'GET', 
        url: '/s/sctable/' + sn,
        dataType: 'json' 
    })
    .then(function(item) {
        $('#frm-public input[name="sn"]').val(item['sn']);
        $('#frm-public input[name="courseno"]').val(item['courseno']);
        $('#frm-public input[name="tno"]').val(item['tno']);
        $('#frm-public input[name="cla"]').val(item['cla']);
        $('#frm-public input[name="week"]').val(item['week']);
        $('#frm-public select[name="weekday"]').val(item['weekday']);
        $('#frm-public select[name="period"]').val(item['period']);
        $('#frm-public select[name="campus"]').val(item['campus']);
        $('#frm-public select[name="building"]').val(item['building']);
        $('#frm-public input[name="croom"]').val(item['croom']);

        $('#frm-public').off('submit').on('submit', put_public);
        $('#frm-public input:submit').val('修改')
        $('#dlg-public-form').show()
    }); 

}

function register_public() {
    // 因为新添和修改都使用和这个表单，因此需要置空这个表单
    $('#frm-public input[name="sn"]').val('');
    $('#frm-public input[name="courseno"]').val('');
    $('#frm-public input[name="tno"]').val('');
    $('#frm-public input[name="cla"]').val('');
    $('#frm-public input[name="week"]').val('');
    $('#frm-public select[name="weekday"]').val('');
    $('#frm-public select[name="period"]').val('');
    $('#frm-public select[name="campus"]').val('');
    $('#frm-public select[name="building"]').val('');
    $('#frm-public input[name="croom"]').val('');
    $('#frm-public input:submit').val('确定')
    // 要先把前面事件处理取消掉，避免累积重复事件处理
    $('#frm-public').off('submit').on('submit', function() {
        var item = {};
        item['term'] = $('#select1 option:selected').text();

        item['courseno'] = $('#frm-public input[name="courseno"]').val();
        item['tno'] = $('#frm-public input[name="tno"]').val();
        item['cla'] = $('#frm-public iput[name="cla"]').val();
        item['week'] = $('#frm-public input[name="week"]').val();
        item['weekday'] = $('#frm-public select[name="weekday"]').val();
        item['period'] = $('#frm-public select[name="period"]').val();
        item['campus'] = $('#frm-public select[name="campus"]').val();
        item['building'] = $('#frm-public select[name="building"]').val();
        item['croom'] = $('#frm-public input[name="croom"]').val();

        $.ajax({ 
            type: 'POST', 
            url: '/s/sctable/',
            data: JSON.stringify(item),
            dataType: 'json' 
        })
        .done(function(){
            load_list();
            $('#dlg-public-form').hide()
        });

        return false; // 在AJAX下，不需要浏览器完成后续的工作。
    });
    $('#dlg-public-form').show()
}

function delete_public(sn) {
    $.ajax({
        type: 'DELETE',
        url: '/s/sctable/' + sn,
        dataType: 'html'
    })
    .done(function() {
        load_list();
    });
}

//----------------------------------------------------
$(document).ready(function() {

	$( "#btn-search" ).on( "click", Termselect);
    $( "#btn-refresh" ).on( "click", load_list);
    $( "#btn-new" ).on( "click", register_public);
    $( "#btn-public-frm-close" ).on( "click", function() {
        // 在关闭浏览器时，可能会自动提交，需要设置一个空提交方法。
        $('#frm-public').off('submit').on('submit', function() {
            return false;
        });
        $('#dlg-public-form').hide();
    });

    load_list();
});

//---设置AJAX缺省的错误处理方式
//---有时需要禁止全局错误处理时，可以在调用ajax时增添{global: false}禁止
$(document).ajaxError(function(event, jqxhr, settings, exception) {
    var msg = jqxhr.status + ': ' + jqxhr.statusText + "\n\n";
    if (jqxhr.status == 404 || jqxhr.status == 405 ) { 
        msg += "访问REST资源时，URL错误或该资源的请求方法\n\n"
        msg += settings.type + '  ' + settings.url  
    } else {
        msg += jqxhr.responseText;
    }
    alert(msg);
});


