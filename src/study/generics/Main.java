package study.generics;

import java.nio.ByteBuffer;

public class Main<T> {

    public static void main(String[] args) {

        StringConverter consumer = new StringConverter();
        StringProducer producer = new StringProducer("Ala ma kota");
        Main<String> stringExample = new Main<>();
        stringExample.example(producer,consumer);


        ByteConverter consumer2 = new ByteConverter();
        ByteProducer producer2 = new ByteProducer("Ala ma kota".getBytes());
        Main<ByteBuffer> byteExample = new Main<>();
        byteExample.example(producer2,consumer2);

    }

    public void example(Producer<T> producer, Converter<T> converter){
        T src = producer.get();
        ByteBuffer dest =  ByteBuffer.allocateDirect(1000);
        converter.transform(src, dest);
        byte[] result = new byte[dest.position()];
        dest.flip();
        dest.get(result);
        System.out.println(new String(result));
    }
}
