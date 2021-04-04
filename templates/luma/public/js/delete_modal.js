
                     $(".deleteButtons").click(
                     function(){
                            // assign the href of the delete-lesson-button to the modal-delete-lesson
                         $("#myModalDeleteButton").attr("href", $(this).attr("value"));
                        $("#myModal").show();
                      });
                     $("#cancel").click(
                     function(){
                          $("#myModal").hide();
                      });
                     $("#close_icon").click(
                     function(){

                          $("#myModal").hide();
                      });

