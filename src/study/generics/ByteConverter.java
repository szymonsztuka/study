package study.generics;

import java.nio.ByteBuffer;

public class ByteConverter implements Converter<ByteBuffer> {
    byte[] transmitter = new byte[200];

    @Override
    public boolean transform(ByteBuffer src, ByteBuffer dest) {
        src.get(transmitter,0, src.limit());
        dest.put(transmitter);
        return src.hasRemaining();
    }
}
