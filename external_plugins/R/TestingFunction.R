    #' An example for writing a function in R using Roxygen (e.g. a variant of Doxygen for
    #' R) 
    #' Well, this function is for writing stuff, I suppose that I need to write here the
    #' pourpose of the function.
    #' @param something Something to put
    #' @keywords Tests, examples, many
    #' @export
    #' @examples
    #' test_function()
    test_function  <- function(something=TRUE) {
      if(something==TRUE) {
       c = 'Something is True'
      return(c)
      }
      else {
        c = 'Something is different from TRUE'
        return(c)
      }
    }


