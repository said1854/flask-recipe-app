$(document).ready(function () {
  console.log("bring!");
  $("#find_button").click(function () {
    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/update_recipe",
      dataType: "json",
      data: JSON.stringify($("#update_input").val()),
      success: function (data) {
        var x = JSON.stringify(data);
        console.log(x);
      },
      error: function (xhr, status, error) {
        console.log("Client Not Found!");
      },
    });
  });
});
