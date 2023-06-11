import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.AllArgsConstructor;

import java.lang.reflect.Type;


public class Data {
    private String Name;
    private String Surname;

    public String getName() {
        return Name;
    }

    public void setName(String Name) {
        this.Name = Name;
    }

    public String getSurname() {
        return Surname;
    }

    public void setSurname(String Surname) {
        this.Surname = Surname;
    }
}

