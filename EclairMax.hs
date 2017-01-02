type Point = (Double, Double)
type Curve = [Point]

dist :: Point -> Point -> Double
dist a b = sqrt ((fst a - fst b)^2 + (snd a - snd b)^2)

-- If everything goes well (ie d(A,B)<r and d(A,C)<r) calls back standard_placing
-- Else, ignores the farthest point and iterates through curve
placing :: Curve -> Double -> Point -> Point -> Curve
-- we made a tweak to limit error : to compute the intersection we always choose the last point that has
-- a distance smaller than r while for placing and standardPlacing we choose the first one to be beyond r
-- otherwise errors due to discretization would add up
placing (p:[]) r a b              =  p:[]
placing (p:ps) r a b
  | dist p a <= r && dist p b > r =  placing ps r a b
  | dist p a <= r                 =  standardPlacing ps r a b
  | otherwise                     =  (p:ps)
  where standardPlacing (p:[]) r a b = p:[]
        standardPlacing (p:ps) r a b = if dist3 p a b <= r then standardPlacing ps r a b else (p:ps)
        dist3 a b c = max (dist a b) (dist a c)

-- Determines the intersection between the circle of center a and the curve
intersection :: Curve -> Double -> Point -> Curve
intersection curve r a  = case curve of
  p:[]      -> p:[]
  p:q:[]    -> q:[]
  p:q:ps    -> if dist q a <= r then intersection (q:ps) r a else p:q:ps
  otherwise -> error "invalid input"

-- Returns the list of lamps
eclair :: Curve -> Curve -> Double -> [Point]
eclair upper lower r = eclaire upper lower False r
-- uses a boolean onTheUpperSide to determine which curve it has to iterate on
eclaire :: Curve -> Curve ->  Bool -> Double -> [Point]
eclaire _ [] _ _ = []
eclaire [] _ _ _ = []
eclaire upper lower onTheUpperSide r = [p]++result
  where a      = if onTheUpperSide then head lower else head upper
        b:uppr = intersection upper r a
        c:lwer = intersection lower r a
        p:ps   = if onTheUpperSide then placing uppr r b c else placing lwer r c b
        result = if onTheUpperSide then eclaire ps lwer (not onTheUpperSide) r
                                   else eclaire uppr ps (not onTheUpperSide) r

-- determines the area of a polygon using the shoelace formula
area :: Curve -> Double
area (p:ps) = abs (sumDet (ps++[p]))/2.0
  where
    sumDet (a:[])   = 0
    sumDet (a:b:ps) = sumDet (b:ps) + (fst a)*(snd b) - (fst b)*(snd a)

-- generates the upper and lower curves which define the road (the idea is we
-- start with a parametric representation of the road and we add it some width, 
-- thus defining two other curves which define the boundaries of the road)
upper :: Curve -> Double -> Curve
upper (p:[]) l   = []
upper (p:q:ps) l = [(fst p - l*dy/n, snd p + l*dx/n)]++(upper (q:ps) l)
  where dx = fst q-(fst p) --the coordinates of the derivative of the curve (namely q-p)
        dy = snd q-(snd p) --thus (-dy, dx) is the vector perpendicular to the middle curve
        n  = sqrt (dx^2 + dy^2) --the norm of (dx,dy)

lower middle l = upper middle (-l)
