package study.generics;

import java.nio.ByteBuffer;

public class ByteProducer implements Producer<ByteBuffer>{

    private final ByteBuffer obj;
    public ByteProducer(byte[] data){
        obj = ByteBuffer.allocateDirect(1000);
        obj.put(data);
        obj.flip();
    }
    @Override
    public ByteBuffer get() {
        return obj;
    }
}
