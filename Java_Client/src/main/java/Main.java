import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.*;
import java.net.Socket;

public class Main {
    private static Socket clientSocket;
    private static BufferedReader reader;
    private static BufferedReader in;
    private static BufferedWriter out;

    public static void main(String[] args) throws IOException {
        clientSocket = new Socket("localhost", 3000);
        reader = new BufferedReader(new InputStreamReader(System.in));
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
        ObjectMapper objectMapper = new ObjectMapper();
        Data data = new Data();
        data.setName("Artem");
        data.setSurname("Myakishev");
        String result = objectMapper.writeValueAsString(data);
        System.out.println(result);
        out.write(result + "\n");
        out.flush();
    }

}
