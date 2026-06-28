import java.security.MessageDigest;
import javax.crypto.Cipher;

public class Legacy {
  void run() throws Exception {
    MessageDigest digest = MessageDigest.getInstance("SHA-1");
    Cipher tripleDes = Cipher.getInstance("DESede/CBC/PKCS5Padding");
    Cipher rc = Cipher.getInstance("RC4");
  }
}
