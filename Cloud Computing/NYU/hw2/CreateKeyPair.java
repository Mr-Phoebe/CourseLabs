import com.amazonaws.services.ec2.AmazonEC2;
import com.amazonaws.services.ec2.AmazonEC2ClientBuilder;
import com.amazonaws.services.ec2.model.CreateKeyPairRequest;
import com.amazonaws.services.ec2.model.CreateKeyPairResult;

public class CreateKeyPair
{
    public final static String keyName = "my-key-pair";

    public static void main(String[] args)
    {
        final AmazonEC2 ec2 = AmazonEC2ClientBuilder.defaultClient();

        CreateKeyPairRequest request = new CreateKeyPairRequest()
            .withKeyName(keyName);

        CreateKeyPairResult response = ec2.createKeyPair(request);

        System.out.printf(
            "Successfulyl created key pair named %s",
            keyName);
    }
}
