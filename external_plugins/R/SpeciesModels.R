#'Pseudo Absences (Naive method)
#'Given two sets: relative_sample and background, returns 0, 1 or NA.
#'This is necessary for defining absences in presence-only data.
# @param relative_sample : the presence of the relative group
# @param background : The entire background sample
#' @export
#' @examples
#' pseudo_absence_naive()

pseudo_absence_naive <- function(relative_sample,background) {
   if ( ! background ) {
        return(NA)
    }
    else if ( relative_sample ) {
        return(1)
    }
    ## insert here in case of something different for 0 (i.e. relative=0 and back =1)
    else {
        return(0)
    }
}

z = rnorm(100)



