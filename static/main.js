$(document).ready(function () {
  // buscar si viene un id en path tenemos que hacer el get
  var id = location.pathname.substring(1);

  // tenemos un id
  if (id.length === 10) {
    $("#c1").removeClass("active");
    $("#m1").removeClass("disabled");
    $("#m1").addClass("active");
    $("#m2").attr("data-toggle", "pill");
    $("#tab1").removeClass("in active");
    $("#tab3").addClass("in active");

    get(id);
  }

  // form1 submit
  $("#form1").submit(function (e) {
    e.preventDefault();
    key = $("#key1").val();
    str = $("#msg1").val();

    var crypt = CryptoJS.AES.encrypt(str, key);
    $("#msg1").val(crypt);

    post();
  });

  // encriptar
  $("#btn2").click(function () {
    key = $("#key2").val();
    str = $("#msg2").val();
    if (!key) {
      alert("Clave vacia");
      return false;
    }
    if (!str) {
      alert("Mensaje vacio");
      return false;
    }
    var crypt = CryptoJS.AES.encrypt(str, key);
    var str2 = crypt
      .toString()
      .replace(/\s/g, "")
      .replace(/(.{64})/g, "$1\n")
      .replace(/\n$/, "");
    $("#msg2").val(str2);
    $("#msg2").focus().select();
  });

  // desencriptar
  $("#btn3").click(function () {
    key = $("#key2").val();
    str = $("#msg2").val();
    if (!key) {
      alert("Clave vacia");
      return false;
    }
    if (!str) {
      alert("Mensaje vacio");
      return false;
    }
    str = str.replace(/(\s+|\r\n|\r|\n)/g, "");
    var crypt = CryptoJS.AES.decrypt(str, key);
    $("#msg2").val(crypt.toString(CryptoJS.enc.Utf8));
  });

  // desencriptar
  $("#btn4").click(function () {
    key = $("#key3").val();
    str = $("#msg3").val();
    if (!key) {
      alert("Clave vacia");
      return false;
    }
    str = str.replace(/(\s+|\r\n|\r|\n)/g, "");
    var crypt = CryptoJS.AES.decrypt(str, key);
    $("#msg3").val(crypt.toString(CryptoJS.enc.Utf8));
  });

  $("ul.nav.nav-pills li a").click(function (e) {
    if (history.pushState) {
      history.pushState(null, null, "/");
    }
  });
});

var get = function (gid) {
  $.get("http://localhost:5100/" + gid, function (data) {
    $("#info").html(data.info);
    $("#msg3").val(data.msg);
  });
};

var post = function () {
  console.log(serializate($("#form1").serializeArray()));
  var datos = serializate($("#form1").serializeArray());
  $.ajax({
    url: "http://localhost:5100/",
    type: "POST",
    headers: { "content-type": "application/json" },
    data: datos,
    success: function (data) {
      $("#postdetail").val(location + data.msgid);
      $("#waitdialog").modal("show");
      $("#waitdialog").on("shown.bs.modal", function (e) {
        $("#postdetail").focus().select();
      });
    },
  });
};

var serializate = function (valor) {
  var retVal = "";
  $.each(valor, function (i, field) {
    retVal += '"' + field.name + '":"' + field.value + '",';
  });
  if (retVal.length > 0) retVal = retVal.substring(0, retVal.length - 1);

  return "{" + retVal + "}";
};
/*
var modal = function(title, content, status) {
    if (status === 'success') {
        $('#poststatus').addClass('label-success');
        $('#poststatus').removeClass('label-danger');
    } else if (status === 'error') {
        $('#poststatus').addClass('label-danger');
        $('#poststatus').removeClass('label-success');
    }

    $('#poststatus').text(title);
    $('#postdetail').val(content);
    $('#postdialog').modal('show');
};

var error = function(title, content) {
    modal(title, content, 'error');
};

var success = function(title, content) {
    modal(title, content, 'success');
};
*/
