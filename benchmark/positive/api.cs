using System.Security.Cryptography;

public class Api {
  public void Run() {
    var provider = new RSACryptoServiceProvider(2048);
    var hasher = MD5.Create();
  }
}
