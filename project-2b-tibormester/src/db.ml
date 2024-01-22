type person = { name: string; age: int; hobbies: string list }

(* Define the type of db below *)
type db = person list

let newDatabase = 
  []

let insert person db = 
  person :: db

let rec remove name db = 
  match db with
  | [] -> []
  | p :: tl ->
    if p.name = name then remove name tl
    else p :: (remove name tl)

type condition =
  | True
  | False
  | Age of (int -> bool)
  | Name of (string -> bool)
  | Hobbies of (string list -> bool)
  | And of condition * condition
  | Or of condition * condition
  | Not of condition
  | If of condition * condition * condition

let rec satisfies condition person = 
  match condition with
  | True -> true
  | False -> false
  | Age pred -> pred person.age
  | Name pred -> pred person.name
  | Hobbies pred -> pred person.hobbies
  | And (c1, c2) -> satisfies c1 person && satisfies c2 person
  | Or (c1, c2) -> satisfies c1 person || satisfies c2 person
  | Not c -> not (satisfies c person)
  | If (c1, c2, c3) -> if satisfies c1 person then satisfies c2 person else satisfies c3 person

let rec query condition db = 
  List.filter (fun person -> satisfies condition person) db;

type comparator = person -> person -> int

let rec sort comparator db = 
  List.sort comparator db

let queryBy condition db comparator = 
  sort comparator (query condition db)

let update condition db personData = 
  List.map (fun p -> if satisfies condition p then personData p else p) db

let deleteAll condition db = 
  List.filter (fun p -> not(satisfies condition p)) db

