using System;
using System.Security;
using System.Security.Permissions;
using BepInEx;
using HarmonyLib;
using UnityEngine;

#pragma warning disable CS0618

[module: UnverifiableCode]
[assembly: SecurityPermission(SecurityAction.RequestMinimum, SkipVerification = true)]

namespace TemplateMod;

[BepInPlugin(ModInfo.PLUGIN_GUID, ModInfo.PLUGIN_NAME, ModInfo.PLUGIN_VERSION)]
[HarmonyPatch(typeof(TemplateMod), MethodType.Constructor)]
public class TemplateMod : BaseUnityPlugin
{
    private Harmony _harmony;

    public TemplateMod()
    {
        _harmony = new Harmony($"{ModInfo.PLUGIN_GUID}");
        UnityEngine.Debug.Log($"{ModInfo.PLUGIN_NAME} constructed!");
    }

    private void Awake()
    {
        UnityEngine.Debug.Log($"{ModInfo.PLUGIN_NAME} patching!");
        _harmony.PatchAll();

        UnityEngine.Debug.Log($"Hello from {ModInfo.PLUGIN_NAME}!");
        UnityEngine.Debug.Log($"Application version is ${Application.version}.");
    }
}