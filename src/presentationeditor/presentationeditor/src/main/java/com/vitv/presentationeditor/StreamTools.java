
package com.vitv.presentationeditor;

import java.io.InputStream;
import java.util.function.Consumer;
import java.util.function.Supplier;
/**
 *
 * @author kpliuniverse
 */
public class StreamTools {

    public static class CondIterator<T> {
        private final Supplier<Boolean> _whileCond;
        private final Supplier<T> _iterator;
        
        public CondIterator(Supplier<Boolean> whileCond, Supplier<T> iterator) {
            _whileCond = whileCond;
            _iterator = iterator;
        }
        public final boolean testCond() {
            return _whileCond.get();
        }
        public final T iterate() {
            return _iterator.get();
        }
    }

    public static <R, T> void forEach(Consumer<T> fn, R stream, CondIterator condIterator)  {
        while (condIterator.testCond()) {
            fn.accept((T) condIterator.iterate());
          }
    }
}
