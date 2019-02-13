library(Rglpk)
library(prodlim)

allAvailableFrames <- c(100, 100, 100, 100, 100)
maxStation <- length(allAvailableFrames)



requestedStations <- sample(1:maxStation, sample(1:maxStation, 1))
requestedNumber <- sample(1:100, 1)

obj <- c(rep(0, maxStation))
obj[requestedStations] <- 1

mat <- matrix(nrow = 0, ncol = maxStation)
dir <- c()
rhs <- c()
types <- c(rep("I", maxStation))
max <- TRUE

bounds <- list(upper = list(ind = c(1:maxStation), val = allAvailableFrames))
glpk <- Rglpk_solve_LP(obj, mat, dir, rhs, bounds, types, max)

if(glpk$optimum >= requestedNumber){
  ## Check if constraints need to be added
  ## cond1 - if not covered as it is, add it
  if(!any(apply(mat, 1, function(x) all(x == obj)))){
    ## Add new constraint as the obj
    mat <- rbind(mat, obj)
    dir <- c(dir, "<=")
    rhs <- c(rhs, (glpk$optimum - requestedNumber))
  }
  
  ## Cond2 - Update constraints for any overlapping stations - this takes care of superset as well
  overlappingConstraintsRow <- which(apply((t(t(mat) * obj)), 1, sum) > 0)
  for(i in 1:len(overlappingConstraintsRow)){
    constraint <- mat[overlappingConstraintsRow[i]]
    overlappingStations <- which(constraint == 1 & obj == 1)
    otherStations <- which(constraint == 0 & obj == 1)
    totalAvailableInOtherStation = maximise() ## Call to basic glpk for other stations iff len(otherStations) > 0 else 0
    if(totalAvailableInOtherStation < requestedNumber){
      excessNumber <- requestedNumber - totalAvailableInOtherStation
      rhs[overlappingConstraintsRow[i]] <- rhs[overlappingConstraintsRow[i]] - excessNumber
    }
    
    ## Creating a universal constraints including existing constraint and obj
    if(len(otherStations) > 0){
      allAvailableInUniversalConstraint <- rhs[overlappingConstraintsRow[i]] + totalAvailableInOtherStation
      allStations <- which(constraint == 1 | obj == 1)
      addConstraint() ## Call to add
    }
  }
  
    
    
  ## Update existing constraint
  ## Reduce constraints
}



requestedStationList <- list(c(2,4), c(2,3,5))
requestedNumberList <- c(33, 86)



obj <- c(3, 1, 3)
mat <- matrix(c(-1, 0, 1, 2, 4, -3, 1, -3, 2), nrow = 3)
dir <- c("<=", "<=", "<=")
rhs <- c(4, 2, 3)
types <- c("I", "I", "I")
max <- TRUE

bounds <- list(lower = list(ind = c(1L, 3L), val = c(-Inf, 2)),
               upper = list(ind = c(1L, 2L), val = c(4, 100)))
Rglpk_solve_LP(obj, mat, dir, rhs, bounds, types, max)



