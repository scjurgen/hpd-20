#include <iostream>
#include <map>

typedef struct
{
   char name[10];
   uint16_t values[59];
}Chain;
#pragma pack(1)

typedef struct
{
    char marker[2];
    char nameUp[12];
    char nameDown[16];
    uint8_t volume;
    uint8_t pedal_hh;
    uint8_t unknown[192];
}Kit;
// 00 00 00 01 11 00 16 01 06 00 00 00 07 02 0A 00 02 03 00 00 00 00 00 00 00 00 00 19 00 00 00 4A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 24 00 05 00 02 00 05 00 14 00 0F 00 0F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 64 00 05 00 06 00 00 00 00 00 00 00 4F 00 0D 00 0F 00 0F 00 1E 00 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 5C 00 1C 00 09 00 0D 00 0F 00 00 00 1B 00 00 00 01 00 00 00 0F 00 07 00 0F 00 00 00 01 00 0F 00 7F 00 00 00 00 00 2A 00 16 00 2C

#pragma pack(1)

typedef struct
{
    uint8_t vol[2];  // 2
    uint8_t amb[2]; // 2   4
    uint8_t patch[2][2]; // 4   8
    uint8_t patchSomehow[2][2]; // 4   12
    uint8_t tuning[2][2];    //  4  16
    int8_t muffling[2];   // 2   18
    int8_t pan[2];        // 6   24
    int8_t unk3[3];
    int8_t color[2];
    int8_t mfx_assign[2];
    int8_t sweep[2];      //     26
    uint8_t unk4[4];  //     46
    uint8_t midi;
    uint8_t midiGate;
    uint8_t unk2;
    uint8_t sendAllpads;
    uint8_t sendToKit;
    uint8_t ukn1;
    uint8_t recPitch;
    uint8_t mute;
    uint8_t rtPitch;
    uint8_t roll;
    uint8_t layer;
    uint8_t fadePoint;
    uint8_t trigger;
    uint8_t unk_1;
    uint8_t fixVol;
    uint8_t fixGroup;
    uint8_t monoPoly;
    uint8_t unknown3[18]; //     68
} Pad;

Chain chains[15];
Kit kits[200];
Pad pads[3400];

void LoadChains(FILE *fp, long seekpos)
{
    fseek(fp, seekpos, SEEK_SET);
    fread(chains, sizeof(chains),1, fp);
}

void LoadKits(FILE *fp, long seekpos)
{
    fseek(fp, seekpos, SEEK_SET);
    fread(kits, sizeof(kits),1, fp);
}

void LoadPads(FILE *fp, long seekpos)
{
    fseek(fp, seekpos, SEEK_SET);
    fread(pads, sizeof(pads),1, fp);
}

void LoadData(const char *fname)
{
    FILE *fp;
    printf("sizeof chains %lu\n", sizeof(chains));
    printf("sizeof kits %lu\n", sizeof(kits));
    printf("sizeof pads %lu\n", sizeof(pads));
    fp = fopen(fname,"rb");
    if (fp)
    {
        LoadChains(fp, 1180);
        LoadKits(fp, 6922);
        LoadPads(fp, 51596);
        fclose(fp);
    }
    else
    {
        printf("couldn't load any set\n");
    }
}

void  DumpValues(uint8_t* p, int size)
{
    for (int i=0; i < size; ++i)
    {
        printf("%02x\t", p[i]);
    }
    printf("\n");
    for (int i=0; i < size; ++i)
    {
        printf("%d\t", p[i]);
    }
    printf("\n");
}

void ShowPadValue(const Pad &pad)
{
    for (int i=0; i < 2; i++) {
        printf("patch %d: %d\n", i, pad.patch[i][1]+(pad.patch[i][0]<<8));
        printf("  vol %d: %d\n", i, pad.vol[i]);
        printf("  pan %d: %d\n", i, pad.pan[i]);
        int t=pad.tuning[i][1]+(pad.tuning[i][0]<<8);
        if (t >=32768)
            t = -(65536-t);
        printf(" tune %d: %+d\n", i, t );
        printf("muffl %d: %d\n", i, pad.muffling[i]);
        printf("sweep %d: %d\n", i, pad.sweep[i]);
    }
}


int main() {
    static_assert(sizeof(Pad) == 68, "68 ");
    LoadData("/Users/scjurgen/Desktop/HPD-20/Backup/BKUP-021.HS0");
    for (int i=0; i < 15; ++i)
    {
        printf("%d %s\n", i+1, chains[i].name);
    }
    for (int i=0; i < 200; ++i)
    {
        printf("%d %s\n", i+1, kits[i].nameUp);
    }


    std::map<int, int> values;
    for (int i=0; i < 3400; ++i)
    {
        for (int j=0; j < 2; ++j) {
            int key =  (pads[i].patch[j][0]<<8) + pads[i].patch[j][1];
            int value = (pads[i].patchSomehow[j][0]<<8)+ pads[i].patchSomehow[j][1];
            auto it = values.find(key);
            if (it != values.end())
            {
                if (it->second != value)
                {
                    printf("[%d %d %d] Some clash on key %d (values %d %d)\n", i/17, i %17, j, key, it->second, value);
                }
            }
            values[key] = value;
        }
            printf("%02x%02x:%02x%02x\n",  pads[i].patch[j][0],pads[i].patch[j][1],pads[i].patchSomehow[j][0], pads[i].patchSomehow[j][1]);
    }
    for (auto item: values)
    {
        printf("%d:%d,\n", item.first, item.second);
    }

/*    int pad = (226288-51596)/68-2;

    pad = 3400-1-17;
    ShowPadValue(pads[pad]);
    for (int i=0; i < 17; ++i)
        DumpValues((uint8_t*)&pads[pad+i], 68);
        */
    return 0;
}
