import logging
import jpype as jp

if not jp.isJVMStarted():
    ZEMBEREK_PATH = 'lib/zemberek-full.jar'
    jp.startJVM(jp.getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

def init_jvm():
    """Initializes the Java virtual machine (JVM).
    :param jvmpath: The path of the JVM. If left empty, inferred by :py:func:`jpype.getDefaultJVMPath`.
    :param max_heap_size: Maximum memory usage limitation (Megabyte). Default is 1024 (1GB). If you set this value too small, you may got out of memory. We recommend that you set it 1024 ~ 2048 or more at least. However, if this value is too large, you may see inefficient memory usage.
    """
    if jp.isJVMStarted():
        jp.attachThreadToJVM()
        return
    ZEMBEREK_PATH = 'lib/zemberek-full.jar'
    jp.startJVM(jp.getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

