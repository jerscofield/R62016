#include <Arduino.h>

//how to I do an array of four different variables? -- enumerated values
char current_side;

int current_node;

const int nodes_per_side = 4;


class obstacle_node{
 
  //should these be private or public?
  public:
 
  boolean on_tunnel;
  boolean dead_end;
  
  //the value of the die in the cache
  //value will be zero if there is no die
  int die_value = 0;
  
  //is this node on the perimeter?
  boolean is_perimeter;
  
  //has the robot trasversed this node yet?
  boolean has_been_here;
  
 //which side of the course is this node on? Only relevant if
 //is_perimeter == true
  char which_side;
};


void searchPerimeter(obstacle_node *a);
 
//update node according to course characteristics
void updateNode(obstacle_node *a);
void nextNode();
boolean is_searching;




//do I need to include function headers for Arduino?

void setup(){
  
  Serial.begin(9600);
  //while(!Serial);
  
  int number_of_nodes = (nodes_per_side*nodes_per_side);
  //create array of Obstacle_nodes
  //need to initiate all of these values to 0.
  obstacle_node course_nodes[number_of_nodes];
  
  
  //mark "is_searching" as true
  is_searching = true;
  
  //initialize first side to 0
  current_side = 's';
  
  //the first node in the grid will always be 1
  //set current_node to 1 -- the first corner of the course
  current_node = 1;
  
  
  //add function: Detect walls
  //add function: face correct direction
  
  //gather data from the perimeter
  searchPerimeter(course_nodes);
  
  Serial.print("Perimeter search complete!");
  /*
  //find tunnel beginning and go there
  for(int i = 1; i < number_of_nodes; i++){
    if(course_nodes[i].on_tunnel){
      //add function: go to beginning of tunnel
      break; //exit the for loop
    }  
  }*/
  while(1);
  

}


void loop(){
  while(true);
  
}


void searchPerimeter(obstacle_node *a){
  //search the perimeter for as long as we haven't returned to the first corner.
  //if we are back at the first corner, exit loop
  while(is_searching){
  //Is there a die cache on this node?
  //If yes, check die cache and update LED
  
  //get and save information and update node data
  updateNode(a);
  
  
  //go to next node
  next_node();
  
  }
  return;
}


void updateNode(obstacle_node *a){
  

  int not_real;

      
    //used for testing
   Serial.println("input a letter for the direction");
  //wait until user input values
  while(!Serial.available());
//    Serial.println("input a letter for the direction");
    not_real = Serial.read();
    a[current_node].which_side == not_real;
    Serial.println(not_real);


  //is there a die?
  //get value from die
  
  //is there a tunnel underneath?
  
  //is there a wire in the tunnel?
  
  //is the tunnel a dead end? -- I might not want to actually add this function.
  
  return;
}

void next_node(){
  
  
  //   Serial.println("5");
     
  //turn left if avc is at a corner
  switch(current_node){
    case(nodes_per_side):           
            current_side = 'e';
            //add function: turn left
            break;
    case(nodes_per_side*nodes_per_side):           
            current_side = 'n';
            //add function: turn left
            break;
    case(nodes_per_side*nodes_per_side + 1 - nodes_per_side):           
            current_side = 'w';
            //add function: turn left
            break;
    case(1 + nodes_per_side):           
            current_side = 's';
            //add function: turn left
            //add function: go straight
            is_searching = false;
            break;
    default:
        //output error message
        break;
  }

  
  //add function: go straight one node

  
     switch(current_side){
      case 's':
        Serial.println("current_side");
        current_node++;
            Serial.println("here");
            break;
      case 'e':
        current_node += nodes_per_side;
        Serial.println("current_sidee");
            break;
      case 'n':
        current_node--;
            break;
      case 'w':
        current_node = current_node - nodes_per_side;
            break;
      default:
        //output error message
        Serial.println("current_sided");
        break;
      }
       
          Serial.println("current_node");
               Serial.println(current_node);
    //           
                         Serial.println("current");
  
  return;

}


//create error functions below:
