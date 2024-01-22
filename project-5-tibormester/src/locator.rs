use std::cmp::Ordering;
use std::collections::HashMap;

pub trait PriorityQueue<T: PartialOrd> {
    fn enqueue(&mut self, ele: T) -> ();
    fn dequeue(&mut self) -> Option<T>;
    fn peek(&self) -> Option<&T>;
}

struct Node<T> {
    priority: i32,
    data: T,
}


impl<T> PartialOrd for Node<T> {
    fn partial_cmp(&self, other: &Node<T>) -> Option<Ordering> {
        self.priority.partial_cmp(&other.priority)
    }
}

impl<T> PartialEq for Node<T> {
    fn eq(&self, other: &Node<T>) -> bool {
        self.priority == other.priority
    }
}

impl<T: PartialOrd> PriorityQueue<T> for Vec<T> {

    fn enqueue(&mut self, ele: T) -> () {
        self.push(ele);
        let mut child_index = self.len() - 1;
        
        while child_index > 0 {
            let parent_index = (child_index - 1) / 2;
            if self[child_index] < self[parent_index] {
                self.swap(child_index, parent_index);
                child_index = parent_index;
            } else {
                break;
            }
        }
    }

    fn dequeue(&mut self) -> Option<T> {
        
        if self.is_empty() {
            return None;
        }

        let last_index = self.len() - 1;
        self.swap(0, last_index);

        let removed_element = self.pop().expect("empty heap :(");
        
        if self.is_empty() {
            return None;
        }

        let mut parent_index = 0;
        let mut l_child_index = 1;
        let mut r_child_index = 2;
        let mut smallest_child_index = 0;
        if self.len() > 2 {
            if self[r_child_index] < self[l_child_index] {
                smallest_child_index = r_child_index;
            }
            else {
                smallest_child_index = l_child_index;
            }
        } else if self.len() == 2 {
            smallest_child_index = l_child_index;
        } else {
            return Some(removed_element);
        }
        while smallest_child_index < last_index {
            if self[parent_index] > self[smallest_child_index] {
                self.swap(parent_index, smallest_child_index);
                parent_index = smallest_child_index;
                l_child_index = parent_index * 2 + 1;
                r_child_index = parent_index * 2 + 2;
                if l_child_index < last_index {
                    if r_child_index < last_index {
                        if self[r_child_index] < self[l_child_index] {
                            smallest_child_index = r_child_index;
                        }
                        else {
                            smallest_child_index = l_child_index;
                        }
                    }
                    else {
                        smallest_child_index = l_child_index;
                    }
                }
                else {
                    smallest_child_index = last_index;
                }
            }
            else {
                smallest_child_index = last_index;
            }
        }

        return Some(removed_element);
    }

    fn peek(&self) -> Option<&T> {
        if self.is_empty() {
            return None;
        }
        return Some(&self[0]);
    }
}

pub fn distance(p1: (i32,i32), p2: (i32,i32)) -> i32 {
    let (x1, y1) = p1;
    let (x2, y2) = p2;
    
    let horizontal_distance = (x2 - x1).abs();
    let vertical_distance = (y2 - y1).abs();
    
    return horizontal_distance + vertical_distance;
}

pub fn target_locator<'a>(allies: &'a HashMap<&String, (i32,i32)>, enemies: &'a HashMap<&String, (i32,i32)>) -> (&'a str,i32,i32) {
    let mut min_distance = i32::MAX;
    let mut target: (&'a str, i32, i32) = ("random", 0, 0);

    for (e_name, e_coords) in enemies {
        let mut closest_a_dist = i32::MAX;
        let mut closest_a: String = String::new();

        /*For each enemy and ally pair calcs distance and stores the closest ally to each enemy*/
        for (ally_name, a_coords) in allies {
            let d = distance(*a_coords, *e_coords);
            if d < closest_a_dist {
                closest_a_dist = d;
                closest_a = ally_name.to_string();
            }
        }

        /*checks if that closest ally is Stark and if this is the closest enemy to stark */
        if closest_a == "Stark" && closest_a_dist < min_distance {
            min_distance = closest_a_dist;
            target = (e_name, e_coords.0, e_coords.1);
        }

    }

    return target;
}


