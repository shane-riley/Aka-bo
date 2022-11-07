import java.io.File;
import java.io.FileWriter;
import java.util.Scanner;

public class App {
    
    public static void main(String[] args) throws Exception {
        
        File state=new File("state.txt");
          // Scanner s =new Scanner(boardFile);
       

    Scanner rFile=new Scanner(state);
    Scanner input=new Scanner(System.in);
    String boardString=rFile.nextLine();
    rFile.close();
    char[] board=new char[42];


    for(int i=0;i<42;i++){
        
        
        board[i]=boardString.charAt(i);
    }
    
    


    System.out.println("Welcome to Connect 4! please type in number 0 through 6 to represent which column you would like to place a piece");


    int column=input.nextInt();
    int check=0;
    int player=Integer.parseInt(boardString.substring(42,43));
    System.out.println(player+"player");
    int decision=Integer.parseInt(boardString.substring(43));
    char piece;
    boardString="";
    
if(decision==0){


   do{
        
        if(player==1){
            piece='r';
            
        }
        else{
            piece='b';
        }

    if(column==0){
        System.out.println("Column 0");
        check=35;
        while(board[check]!='+'||check<0){
            check-=7;
        }
        board[check]=piece;
        System.out.println(piece);
       player*=-1;
    //    column=input.nextInt();
    }
    else if(column==1){
        System.out.println("Column 1");
        check=36;
        while(board[check]!='+'||check<0){
            check-=7;
        }
        board[check]=piece;

        player*=-1;
        // column=input.nextInt();
    }
    else if(column==2){
        System.out.println("Column 2");
        check=37;
        while(board[check]!='+'||check<0){
            check-=7;
        }
        board[check]=piece;

        player*=-1;
        // column=input.nextInt();
    }
    else if(column==3){
        System.out.println("Column 3");
        check=38;
        while(board[check]!='+'||check<0){
            check-=7;
        }
        board[check]=piece;
        player*=-1;
        // column=input.nextInt();
    }
    else if(column==4){
        System.out.println("Column 4");
        check=39;
        player*=-1;
        // column=input.nextInt();
    }
    else if(column==5){
        System.out.println("Column 5");
        check=40;
        while(board[check]!='+'||check<0){
            check-=7;
        }
        board[check]=piece;
        player*=-1;
        // column=input.nextInt();
    }
    else if(column==6){
        System.out.println("Column 6");
        check=41;
        while(board[check]!='+'||check<0){
            check-=7;
        }
        board[check]=piece;
        player*=-1;
        // column=input.nextInt();
    }
    else{
        System.out.println("invalid");
        column=input.nextInt();
    }
}while(column==8);
    
    for(int i=0;i<42;i++){
        // if(i%7==0){
        //     boardString+="\n";
        // }
        boardString+=board[i];

    }
    if(player==0){
        player=1;
    }
    else{
        player=0;
    }
    // player=player*-1;
    boardString+=""+player+""+decision;
    input.close();
    // rFile.remove();
    new FileWriter("state.txt", false).close();
    FileWriter writer=new FileWriter(state);
    System.out.println(boardString);
    writer.write(boardString);
    writer.close();



    



}
else{
    System.out.println("Game over");
}
    }



}


    

