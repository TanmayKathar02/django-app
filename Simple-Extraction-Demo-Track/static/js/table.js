$(document).ready(function () {
  resize();
});
$(window).resize(function () {
  resize();
});
$('#table_id').DataTable();

function resize() {
  var mobileMaxWidth = 640; //Define this to whatever size you want
  if ($(window).width() > mobileMaxWidth) {
    $('#desktop-table').show();
    $('#mobile-table').hide();
    console.log("desktop view")
  } else {
    $('#desktop-table').hide();
    $('#mobile-table').show();
    console.log("mobile view")
  }
}
$(".dataTables_wrapper > .dataTables_filter input").addClass('shadow-lg')
$(".dataTables_wrapper > .dataTables_filter input").css({
  border: "none !important",
  height: "2.5rem"
})