import com.amazonaws.services.ec2.AmazonEC2;
import com.amazonaws.services.ec2.AmazonEC2ClientBuilder;
import com.amazonaws.services.ec2.model.RunInstancesRequest;
import com.amazonaws.services.ec2.model.RunInstancesResult;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.ec2.model.DescribeInstancesRequest;
import com.amazonaws.services.ec2.model.DescribeInstancesResult;
import com.amazonaws.services.ec2.model.Instance;
import com.amazonaws.services.ec2.model.Reservation;

public class CreateEC2Instance {
    public final static String ami_id = "ami-66506c1c";

    private static void create() {

        RunInstancesRequest runInstancesRequest =
                new RunInstancesRequest();

        runInstancesRequest.withImageId(ami_id)
                .withInstanceType("t2.micro")
                .withMinCount(1)
                .withMaxCount(1)
                .withKeyName(CreateKeyPair.keyName)
                .withSecurityGroups(CreateSecurityGroupApp.groupname);


        AmazonEC2 ec2 = AmazonEC2ClientBuilder.standard()
                .withRegion(Regions.US_EAST_1).build();

        RunInstancesResult runInstancesResult = ec2.runInstances(runInstancesRequest);

        Instance instance = runInstancesResult.getReservation().getInstances().get(0);

        System.out.printf(
                "Found instance with id %s, \n" +
                        "AMI %s, \n" +
                        "type %s, \n" +
                        "Private IP address %s, \n" +
                        "Public IP address %s, \n" +
                        "Region %s" +
                        "state %s, \n" +
                        "and monitoring state %s\n",
                instance.getInstanceId(),
                instance.getImageId(),
                instance.getInstanceType(),
                instance.getPrivateIpAddress(),
                instance.getPublicIpAddress(),
                instance.getPlacement().getAvailabilityZone(),
                instance.getState().getName(),
                instance.getMonitoring().getState());

    }

    private static void show() {
        final AmazonEC2 ec2 = AmazonEC2ClientBuilder.defaultClient();
        boolean done = false;

        DescribeInstancesRequest request = new DescribeInstancesRequest();
        while(!done) {
            DescribeInstancesResult response = ec2.describeInstances(request);

            for(Reservation reservation : response.getReservations()) {
                for(Instance instance : reservation.getInstances()) {
                    System.out.printf(
                            "Found instance with id %s, \n" +
                                    "AMI %s, \n" +
                                    "type %s, \n" +
                                    "Private IP address %s, \n" +
                                    "Public IP address %s, \n" +
                                    "Region %s" +
                                    "state %s, \n" +
                                    "and monitoring state %s\n" +
                                    "----------------\n",
                            instance.getInstanceId(),
                            instance.getImageId(),
                            instance.getInstanceType(),
                            instance.getPrivateIpAddress(),
                            instance.getPublicIpAddress(),
                            instance.getPlacement().getAvailabilityZone(),
                            instance.getState().getName(),
                            instance.getMonitoring().getState());
                }
            }

            request.setNextToken(response.getNextToken());

            if(response.getNextToken() == null) {
                done = true;
            }
        }
    }

    public static void main(String[] args) {
        create();
        show();
    }
}
