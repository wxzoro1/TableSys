
function render_list(list) {
    var tbody =  $("#list-tbody").empty();
    for (i in list) {
        var public = list[i];

        var row = $('<tr>');
        $('<td>').text(parseInt(i) + 1).appendTo(row);
        $('<td>').text(public['sno']).appendTo(row);
        $('<td>').text(public['sname']).appendTo(row);
        $('<td>').text(public['gender']).appendTo(row);
        $('<td>').text(public['cla']).appendTo(row);
        $('<td>').text(public['major']).appendTo(row);
        $('<td>').text(public['institute']).appendTo(row);
        $('<td>').text(public['enrolled']).appendTo(row);
         
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
  		url: "/s/student/",
        data: '',
        dataType: 'json' 
	})
    .done(function(data) {
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
        item['sno'] = $('#frm-public input[name="sno"]').val();
        item['sname'] = $('#frm-public input[name="sname"]').val();
        item['gender'] = $('#frm-public select[name="gender"]').val();
        item['cla'] = $('#frm-public input[name="cla"]').val();
        item['major'] = $('#frm-public input[name="major"]').val();
        item['institute'] = $('#frm-public input[name="institute"]').val();
        item['enrolled'] = $('#frm-public input[name="enrolled"]').val();
        var jsondata = JSON.stringify(item);
        $.ajax({ 
            type: 'PUT', 
            url: '/s/student/' + sn,
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
        url: '/s/student/' + sn,
        dataType: 'json' 
    })
    .then(function(item) {
        $('#frm-public input[name="sn"]').val(item['sn']);
        $('#frm-public input[name="sno"]').val(item['sno']);
        $('#frm-public input[name="sname"]').val(item['sname']);
        $('#frm-public select[name="gender"]').val(item['gender']);
        $('#frm-public input[name="cla"]').val(item['cla']);
        $('#frm-public input[name="major"]').val(item['major']);
        $('#frm-public input[name="institute"]').val(item['institute']);
        $('#frm-public input[name="enrolled"]').val(item['enrolled']);
        $('#frm-public').off('submit').on('submit', put_public);
        $('#frm-public input:submit').val('修改')
        $('#dlg-public-form').show()
    }); 

}

function register_public() {
    // 因为新添和修改都使用和这个表单，因此需要置空这个表单
    $('#frm-public input[name="sn"]').val('');
    $('#frm-public input[name="sno"]').val('');
    $('#frm-public input[name="sname"]').val('');
    $('#frm-public select[name="gender"]').val('');
    $('#frm-public input[name="cla"]').val('');
    $('#frm-public input[name="major"]').val('');
    $('#frm-public input[name="institute"]').val('');
    $('#frm-public input[name="enrolled"]').val('');
    $('#frm-public input:submit').val('确定')
    // 要先把前面事件处理取消掉，避免累积重复事件处理
    $('#frm-public').off('submit').on('submit', function() {
        var item = {};
        item['sno'] = $('#frm-public input[name="sno"]').val();
        item['sname'] = $('#frm-public input[name="sname"]').val();
        item['gender'] = $('#frm-public select[name="gender"]').val();
        item['cla'] = $('#frm-public input[name="cla"]').val();
        item['major'] = $('#frm-public input[name="major"]').val();
        item['institute'] = $('#frm-public input[name="institute"]').val();
        item['enrolled'] = $('#frm-public input[name="enrolled"]').val();
        $.ajax({ 
            type: 'POST', 
            url: '/s/student/',
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
        url: '/s/student/' + sn,
        dataType: 'html'
    })
    .done(function() {
        load_list();
    });
}

//----------------------------------------------------
$(document).ready(function() {
	
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


