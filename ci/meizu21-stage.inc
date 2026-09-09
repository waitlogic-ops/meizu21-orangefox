// MEIZU21_STARTUP_DIAGNOSTICS: startup-only overlay, independent of UI fonts.
static bool meizu21_stage_visible = false;
extern "C" void gui_meizu21_stage(int stage, const char* name) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    printf("MEIZU21_STAGE %02d %s pid=%d monotonic=%lld.%03ld\n", stage, name,
           getpid(), (long long)now.tv_sec, now.tv_nsec / 1000000);
    fflush(stdout);
    char value[12];
    snprintf(value, sizeof(value), "%02d", stage);
    property_set("meizu21.boot.stage", value);
    if (!meizu21_stage_visible) return;
    const int width = gr_fb_width();
    const int height = gr_fb_height();
    if (width < 100 || height < 100 || stage < 0 || stage > 99) return;
    int unit = width / 60;
    if (unit < 4) unit = 4;
    if (unit > 24) unit = 24;
    // Two bitmap digits need neither font files nor main UI resources.
    static const char* digits[] = {
        "111101101101111", "010110010010111", "111001111100111",
        "111001111001111", "101101111001001", "111100111001111",
        "111100111101111", "111001001001001", "111101111101111",
        "111101111001111"
    };
    gr_noclip();
    gr_color(0, 0, 0, 255);
    gr_fill(0, 0, unit * 11, unit * 9);
    gr_color(255, 160, 40, 255);
    for (int digit = 0; digit < 2; ++digit) {
        const char* bitmap = digits[digit == 0 ? stage / 10 : stage % 10];
        for (int i = 0; i < 15; ++i) {
            if (bitmap[i] == '1')
                gr_fill((2 + digit * 4 + i % 3) * unit,
                        (2 + i / 3) * unit, unit, unit);
        }
    }
    gr_flip();
}
extern "C" void gui_meizu21_stage_done(void) {
    meizu21_stage_visible = false;
}

